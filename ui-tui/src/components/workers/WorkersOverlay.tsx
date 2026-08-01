import { Box, Text, useInput } from '@pixel-agents/ink'
import { useCallback, useEffect, useMemo, useState } from 'react'

import type { GatewayClient } from '../../gatewayClient.js'
import type { Theme } from '../../theme.js'
import { TextInput } from '../textInput.js'

import { ReviewInbox, type Task } from './ReviewInbox.js'
import { StaffDirectory, type Worker } from './StaffDirectory.js'

interface AgentTemplate {
  id: string
  name: string
}

interface WorkersOverlayProps {
  gw: GatewayClient
  onClose: () => void
  t: Theme
}

type Tab = 'review' | 'staff'
type Mode = 'autonomous' | 'manual' | 'smart'

const nextMode = (mode: string): Mode =>
  mode === 'manual' ? 'smart' : mode === 'smart' ? 'autonomous' : 'manual'

export function WorkersOverlay({ gw, onClose, t }: WorkersOverlayProps) {
  const [tab, setTab] = useState<Tab>('staff')
  const [workers, setWorkers] = useState<Worker[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [catalog, setCatalog] = useState<AgentTemplate[]>([])
  const [cursor, setCursor] = useState(0)
  const [catalogCursor, setCatalogCursor] = useState(0)
  const [hiring, setHiring] = useState(false)
  const [rejectTaskId, setRejectTaskId] = useState<string | null>(null)
  const [feedback, setFeedback] = useState('')
  const [archiveArmed, setArchiveArmed] = useState<string | null>(null)
  const [flash, setFlash] = useState('')
  const [loading, setLoading] = useState(true)

  const pending = useMemo(() => tasks.filter(task => task.status === 'waiting_approval'), [tasks])
  const rows = tab === 'staff' ? workers : pending

  const refresh = useCallback(
    async (quiet = false) => {
      if (!quiet) {
        setLoading(true)
      }

      try {
        const [workerResponse, taskResponse, catalogResponse] = await Promise.all([
          gw.request<{ workers?: Worker[] }>('workers.list', {}),
          gw.request<{ tasks?: Task[] }>('tasks.list', {}),
          gw.request<{ catalog?: AgentTemplate[] }>('agents.catalog', {})
        ])

        setWorkers(workerResponse?.workers ?? [])
        setTasks(taskResponse?.tasks ?? [])
        setCatalog(catalogResponse?.catalog ?? [])
        setFlash('')
      } catch (error) {
        setFlash(error instanceof Error ? error.message : String(error))
      } finally {
        setLoading(false)
      }
    },
    [gw]
  )

  useEffect(() => {
    void refresh()
    const timer = setInterval(() => void refresh(true), 3_000)

    return () => clearInterval(timer)
  }, [refresh])

  useEffect(() => {
    setCursor(current => Math.max(0, Math.min(current, Math.max(0, rows.length - 1))))
  }, [rows.length])

  const run = useCallback(
    async (label: string, action: () => Promise<unknown>) => {
      try {
        await action()
        setFlash(label)
        await refresh(true)
      } catch (error) {
        setFlash(error instanceof Error ? error.message : String(error))
      }
    },
    [refresh]
  )

  const approve = (taskId: string) =>
    void run('work approved', () => gw.request('tasks.approve', { task_id: taskId }))

  const reject = (taskId: string, note: string) =>
    void run('changes requested · task queued again', () =>
      gw.request('tasks.reject', { feedback: note, task_id: taskId })
    )

  useInput((ch, key) => {
    if (rejectTaskId) {
      if (key.escape) {
        setRejectTaskId(null)
        setFeedback('')
      }

      return
    }

    if (hiring) {
      if (key.escape) {
        return setHiring(false)
      }

      if (key.upArrow || ch === 'k') {
        return setCatalogCursor(value => Math.max(0, value - 1))
      }

      if (key.downArrow || ch === 'j') {
        return setCatalogCursor(value => Math.min(Math.max(0, catalog.length - 1), value + 1))
      }

      if (key.return && catalog[catalogCursor]) {
        const template = catalog[catalogCursor]
        const workerId = `${template.id}-${Date.now().toString(36)}`

        setHiring(false)
        void run(`hired ${template.name}`, () =>
          gw.request('workers.hire', {
            autonomy_mode: 'smart',
            display_name: template.name,
            template_id: template.id,
            worker_id: workerId
          })
        )
      }

      return
    }

    if (key.escape || ch === 'q') {
      return onClose()
    }

    if (key.tab || ch === '1' || ch === '2') {
      setTab(ch === '2' ? 'review' : ch === '1' ? 'staff' : tab === 'staff' ? 'review' : 'staff')
      setCursor(0)

      return
    }

    if (key.upArrow || ch === 'k') {
      return setCursor(value => Math.max(0, value - 1))
    }

    if (key.downArrow || ch === 'j') {
      return setCursor(value => Math.min(Math.max(0, rows.length - 1), value + 1))
    }

    if (ch === 'r') {
      return void refresh()
    }

    if (tab === 'staff') {
      const worker = workers[cursor]

      if (ch === 'h') {
        setCatalogCursor(0)

        return setHiring(true)
      }

      if (!worker) {
        return
      }

      if (ch === 'm') {
        const autonomyMode = nextMode(worker.autonomy_mode)

        return void run(`mode · ${autonomyMode}`, () =>
          gw.request('workers.update', {
            updates: { autonomy_mode: autonomyMode },
            worker_id: worker.worker_id
          })
        )
      }

      if (ch === 'p' && worker.status !== 'working') {
        const status = worker.status === 'paused' ? 'idle' : 'paused'

        return void run(status === 'paused' ? 'worker paused' : 'worker resumed', () =>
          gw.request('workers.update', { updates: { status }, worker_id: worker.worker_id })
        )
      }

      if (ch === 'a' && worker.status !== 'working') {
        if (archiveArmed !== worker.worker_id) {
          setArchiveArmed(worker.worker_id)
          setFlash('press a again to archive this worker')

          return
        }

        setArchiveArmed(null)

        return void run('worker archived', () => gw.request('workers.archive', { worker_id: worker.worker_id }))
      }

      return
    }

    const task = pending[cursor]

    if (!task) {
      return
    }

    if (ch === 'y') {
      return approve(task.id)
    }

    if (ch === 'n') {
      setFeedback('')
      setRejectTaskId(task.id)
    }
  })

  if (hiring) {
    return (
      <Box flexDirection="column" flexGrow={1} paddingX={1} paddingY={1}>
        <Text bold color={t.color.accent}>Hire a persistent worker</Text>
        <Text color={t.color.muted}>↑/↓ choose role · enter hire in smart mode · esc cancel</Text>
        <Box flexDirection="column" marginTop={1}>
          {catalog.map((template, index) => (
            <Text color={index === catalogCursor ? t.color.primary : t.color.text} key={template.id}>
              {index === catalogCursor ? '›' : ' '} {template.name} <Text color={t.color.muted}>({template.id})</Text>
            </Text>
          ))}
          {!catalog.length ? <Text color={t.color.muted}>No enabled worker templates.</Text> : null}
        </Box>
      </Box>
    )
  }

  return (
    <Box flexDirection="column" flexGrow={1} paddingX={1} paddingY={1}>
      <Box flexDirection="column" marginBottom={1}>
        <Text bold color={t.color.accent}>AI Office</Text>
        <Text color={t.color.muted}>
          <Text color={tab === 'staff' ? t.color.primary : t.color.muted}>1 Staff ({workers.length})</Text>
          {' · '}
          <Text color={tab === 'review' ? t.color.primary : t.color.muted}>2 Review ({pending.length})</Text>
          {' · tab switch · r refresh · q close'}
        </Text>
      </Box>

      {loading ? <Text color={t.color.muted}>Loading office…</Text> : null}
      {!loading && tab === 'staff' ? <StaffDirectory selectedIndex={cursor} workers={workers} /> : null}
      {!loading && tab === 'review' ? (
        <ReviewInbox onApprove={approve} onReject={reject} selectedIndex={cursor} tasks={pending} />
      ) : null}

      {rejectTaskId ? (
        <Box borderColor={t.color.warn} borderStyle="round" flexDirection="column" marginTop={1} paddingX={1}>
          <Text color={t.color.warn}>Explain what must change, then press Enter · esc cancel</Text>
          <TextInput
            color={t.color.text}
            focus
            onChange={setFeedback}
            onSubmit={value => {
              const note = value.trim()

              if (!note) {
                return setFlash('feedback is required')
              }

              const taskId = rejectTaskId
              setRejectTaskId(null)
              setFeedback('')
              reject(taskId, note)
            }}
            placeholder="Required review feedback"
            value={feedback}
          />
        </Box>
      ) : null}

      <Box marginTop={1}>
        <Text color={flash ? t.color.warn : t.color.muted}>
          {flash || (tab === 'staff' ? 'h hire · m autonomy · p pause/resume · a archive' : 'y approve · n reject')}
        </Text>
      </Box>
    </Box>
  )
}
