import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { useGatewayRequest } from '@/app/gateway/hooks/use-gateway-request'
import { Button } from '@/components/ui/button'
import { ErrorState } from '@/components/ui/error-state'
import { Input } from '@/components/ui/input'
import { Loader } from '@/components/ui/loader'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { useI18n } from '@/i18n'
import { cn } from '@/lib/utils'

export type OfficeTab = 'live' | 'review' | 'staff'
type AutonomyMode = 'autonomous' | 'manual' | 'smart'

interface Worker {
  archived: boolean
  autonomy_mode: AutonomyMode
  display_name: string
  manager_id?: null | string
  status: string
  template_id: string
  worker_id: string
}

interface WorkerTask {
  acceptance_criteria?: null | string
  deliverable?: null | string
  goal: string
  id: string
  last_error?: null | string
  result?: null | string
  status: string
  worker_id: string
  worker_name?: null | string
}

interface AgentTemplate {
  description?: string
  id: string
  name: string
}

interface OfficeData {
  catalog: AgentTemplate[]
  tasks: WorkerTask[]
  workers: Worker[]
}

const emptyData: OfficeData = { catalog: [], tasks: [], workers: [] }

function safeWorkerId(templateId: string): string {
  return `${templateId}-${Date.now().toString(36)}`.replace(/[^a-zA-Z0-9_-]/g, '-').slice(0, 64)
}

function parseCriteria(value?: null | string): string[] {
  if (!value) {
    return []
  }

  try {
    const parsed = JSON.parse(value) as unknown

    return Array.isArray(parsed) ? parsed.map(String) : [String(parsed)]
  } catch {
    return [value]
  }
}

function useOfficeData(active: boolean) {
  const { requestGateway } = useGatewayRequest()
  const [data, setData] = useState<OfficeData>(emptyData)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const generation = useRef(0)

  const refresh = useCallback(
    async (quiet = false) => {
      const current = ++generation.current

      if (!quiet) {
        setLoading(true)
      }

      try {
        const [workersResult, tasksResult, catalogResult] = await Promise.all([
          requestGateway<{ workers?: Worker[] }>('workers.list', {}),
          requestGateway<{ tasks?: WorkerTask[] }>('tasks.list', {}),
          requestGateway<{ catalog?: AgentTemplate[] }>('agents.catalog', {})
        ])

        if (current !== generation.current) {
          return
        }

        setData({
          catalog: catalogResult.catalog ?? [],
          tasks: tasksResult.tasks ?? [],
          workers: workersResult.workers ?? []
        })
        setError(null)
      } catch (cause) {
        if (current === generation.current) {
          setError(cause instanceof Error ? cause.message : String(cause))
        }
      } finally {
        if (current === generation.current) {
          setLoading(false)
        }
      }
    },
    [requestGateway]
  )

  // eslint-disable-next-line no-restricted-syntax -- request generation token, not a mirrored reactive value
  useEffect(() => {
    if (!active) {
      return
    }

    void refresh()
    const interval = window.setInterval(() => void refresh(true), 4_000)

    return () => {
      window.clearInterval(interval)
      generation.current += 1
    }
  }, [active, refresh])

  return { data, error, loading, refresh, requestGateway }
}

export function OfficeView({ tab }: { tab: Exclude<OfficeTab, 'live'> }) {
  const office = useOfficeData(true)
  const { t } = useI18n()

  if (office.loading && office.data.workers.length === 0 && office.data.tasks.length === 0) {
    return (
      <div className="grid min-h-0 flex-1 place-items-center">
        <Loader label={t.agents.office.loading} type="lemniscate-bloom" />
      </div>
    )
  }

  if (office.error && office.data.workers.length === 0 && office.data.tasks.length === 0) {
    return (
      <ErrorState description={office.error} title={t.agents.office.loadFailed}>
        <Button onClick={() => void office.refresh()} variant="secondary">
          {t.common.retry}
        </Button>
      </ErrorState>
    )
  }

  return tab === 'staff' ? <StaffDirectory office={office} /> : <ReviewInbox office={office} />
}

import { AssignTaskModal } from './assign-task-modal'
import { WorkerDetailDrawer } from './worker-detail-drawer'

type OfficeHook = ReturnType<typeof useOfficeData>

function StaffDirectory({ office }: { office: OfficeHook }) {
  const { t } = useI18n()
  const copy = t.agents.office
  const [templateId, setTemplateId] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [mode, setMode] = useState<AutonomyMode>('smart')
  const [busyId, setBusyId] = useState<string | null>(null)
  const [archiveCandidate, setArchiveCandidate] = useState<string | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)
  const [selectedWorkerForDetail, setSelectedWorkerForDetail] = useState<Worker | null>(null)
  const [selectedWorkerForTask, setSelectedWorkerForTask] = useState<Worker | null>(null)

  const selectedTemplate = office.data.catalog.find(template => template.id === templateId)

  useEffect(() => {
    if (!templateId && office.data.catalog[0]) {
      setTemplateId(office.data.catalog[0].id)
    }
  }, [office.data.catalog, templateId])

  const mutate = async (workerId: string, action: () => Promise<unknown>) => {
    setBusyId(workerId)
    setActionError(null)

    try {
      await action()
      await office.refresh(true)
    } catch (cause) {
      setActionError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusyId(null)
    }
  }

  const hire = async () => {
    if (!templateId) {
      return
    }

    const workerId = safeWorkerId(templateId)
    await mutate(workerId, () =>
      office.requestGateway('workers.hire', {
        autonomy_mode: mode,
        display_name: displayName.trim() || selectedTemplate?.name || templateId,
        template_id: templateId,
        worker_id: workerId
      })
    )
    setDisplayName('')
  }

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden">
      <div className="flex shrink-0 flex-wrap items-end gap-2">
        <label className="grid min-w-44 gap-1 text-[0.65rem] text-muted-foreground">
          {copy.role}
          <Select onValueChange={setTemplateId} value={templateId}>
            <SelectTrigger size="sm">
              <SelectValue placeholder={copy.chooseRole} />
            </SelectTrigger>
            <SelectContent>
              {office.data.catalog.map(template => (
                <SelectItem key={template.id} value={template.id}>
                  {template.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </label>
        <label className="grid min-w-40 flex-1 gap-1 text-[0.65rem] text-muted-foreground">
          {copy.name}
          <Input
            onChange={event => setDisplayName(event.target.value)}
            placeholder={selectedTemplate?.name ?? copy.namePlaceholder}
            size="sm"
            value={displayName}
          />
        </label>
        <ModeSelect disabled={Boolean(busyId)} onChange={setMode} value={mode} />
        <Button disabled={!templateId || Boolean(busyId)} onClick={() => void hire()} size="sm">
          {copy.hire}
        </Button>
      </div>

      {actionError ? <p className="shrink-0 text-xs text-destructive">{actionError}</p> : null}

      {office.data.workers.length === 0 ? (
        <div className="grid flex-1 place-items-center text-center">
          <div className="grid gap-1">
            <p className="text-sm font-medium text-foreground/90">{copy.noWorkers}</p>
            <p className="text-xs text-muted-foreground/75">{copy.noWorkersDesc}</p>
          </div>
        </div>
      ) : (
        <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain">
          <div className="grid gap-2">
            {office.data.workers.map(worker => {
              const busy = busyId === worker.worker_id
              const confirmingArchive = archiveCandidate === worker.worker_id

              return (
                <div
                  className="flex flex-wrap items-center gap-3 rounded-md px-2 py-2 hover:bg-(--chrome-action-hover)"
                  key={worker.worker_id}
                >
                  <span
                    aria-hidden
                    className={cn(
                      'size-2 shrink-0 rounded-full',
                      worker.status === 'working'
                        ? 'bg-primary'
                        : worker.status === 'error'
                          ? 'bg-destructive'
                          : worker.status === 'paused'
                            ? 'bg-muted-foreground/50'
                            : 'bg-emerald-500/80'
                    )}
                  />
                  <div className="min-w-40 flex-1">
                    <p className="text-xs font-medium text-foreground/90">{worker.display_name}</p>
                    <p className="font-mono text-[0.65rem] text-muted-foreground/65">
                      {worker.template_id} · {worker.status}
                    </p>
                  </div>
                  {confirmingArchive ? (
                    <div className="flex items-center gap-1.5">
                      <span className="text-[0.68rem] text-muted-foreground">{copy.archiveConfirm}</span>
                      <Button onClick={() => setArchiveCandidate(null)} size="xs" variant="text">
                        {t.common.cancel}
                      </Button>
                      <Button
                        disabled={busy}
                        onClick={() =>
                          void mutate(worker.worker_id, () =>
                            office.requestGateway('workers.archive', { worker_id: worker.worker_id })
                          ).then(() => setArchiveCandidate(null))
                        }
                        size="xs"
                        variant="destructive"
                      >
                        {copy.archive}
                      </Button>
                    </div>
                  ) : (
                    <>
                      <ModeSelect
                        disabled={busy}
                        onChange={next =>
                          void mutate(worker.worker_id, () =>
                            office.requestGateway('workers.update', {
                              updates: { autonomy_mode: next },
                              worker_id: worker.worker_id
                            })
                          )
                        }
                        value={worker.autonomy_mode}
                      />
                      <Button
                        disabled={busy || worker.status === 'working'}
                        onClick={() =>
                          void mutate(worker.worker_id, () =>
                            office.requestGateway('workers.update', {
                              updates: { status: worker.status === 'paused' ? 'idle' : 'paused' },
                              worker_id: worker.worker_id
                            })
                          )
                        }
                        size="xs"
                        variant="secondary"
                      >
                        {worker.status === 'paused' ? copy.resume : copy.pause}
                      </Button>
                      <Button
                        disabled={busy || worker.status === 'working'}
                        onClick={() => setArchiveCandidate(worker.worker_id)}
                        size="xs"
                        variant="text"
                      >
                        {copy.archive}
                      </Button>
                      <Button
                        disabled={busy}
                        onClick={(e) => {
                          e.stopPropagation()
                          setSelectedWorkerForTask(worker)
                        }}
                        size="xs"
                        variant="default"
                      >
                        {t.agents.office.assignTask || 'Assign Task'}
                      </Button>
                      <Button
                        onClick={() => setSelectedWorkerForDetail(worker)}
                        size="xs"
                        variant="secondary"
                      >
                        Details
                      </Button>
                    </>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
      
      {selectedWorkerForTask && (
        <AssignTaskModal
          worker={selectedWorkerForTask as any}
          onClose={() => setSelectedWorkerForTask(null)}
          onSubmit={async (taskParams) => {
            await office.requestGateway('tasks.create', taskParams)
            await office.refresh(true)
          }}
        />
      )}
      
      {selectedWorkerForDetail && (
        <WorkerDetailDrawer
          worker={selectedWorkerForDetail as any}
          tasks={office.data.tasks.filter(t => t.worker_id === selectedWorkerForDetail.worker_id) as any}
          onClose={() => setSelectedWorkerForDetail(null)}
          onAssignTask={(w) => {
            setSelectedWorkerForDetail(null)
            setSelectedWorkerForTask(w as any)
          }}
        />
      )}
    </div>
  )
}

function ModeSelect({
  disabled,
  onChange,
  value
}: {
  disabled?: boolean
  onChange: (mode: AutonomyMode) => void
  value: AutonomyMode
}) {
  const { t } = useI18n()
  const copy = t.agents.office

  return (
    <label className="grid min-w-32 gap-1 text-[0.65rem] text-muted-foreground">
      {copy.mode}
      <Select disabled={disabled} onValueChange={next => onChange(next as AutonomyMode)} value={value}>
        <SelectTrigger size="sm">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="manual">{copy.manual}</SelectItem>
          <SelectItem value="smart">{copy.smart}</SelectItem>
          <SelectItem value="autonomous">{copy.autonomous}</SelectItem>
        </SelectContent>
      </Select>
    </label>
  )
}

function ReviewInbox({ office }: { office: OfficeHook }) {
  const { t } = useI18n()
  const copy = t.agents.office
  const [feedback, setFeedback] = useState<Record<string, string>>({})
  const [busyId, setBusyId] = useState<string | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)

  const pending = useMemo(
    () => office.data.tasks.filter(task => task.status === 'waiting_approval'),
    [office.data.tasks]
  )

  const review = async (task: WorkerTask, action: 'approve' | 'reject') => {
    const note = feedback[task.id]?.trim() ?? ''

    if (action === 'reject' && !note) {
      setActionError(copy.feedbackRequired)

      return
    }

    setBusyId(task.id)
    setActionError(null)

    try {
      await office.requestGateway(action === 'approve' ? 'tasks.approve' : 'tasks.reject', {
        feedback: action === 'reject' ? note : undefined,
        task_id: task.id
      })
      setFeedback(current => ({ ...current, [task.id]: '' }))
      await office.refresh(true)
    } catch (cause) {
      setActionError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusyId(null)
    }
  }

  if (pending.length === 0) {
    return (
      <div className="grid flex-1 place-items-center text-center">
        <div className="grid gap-1">
          <p className="text-sm font-medium text-foreground/90">{copy.inboxEmpty}</p>
          <p className="text-xs text-muted-foreground/75">{copy.inboxEmptyDesc}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-hidden">
      {actionError ? <p className="shrink-0 text-xs text-destructive">{actionError}</p> : null}
      <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain">
        <div className="grid gap-5">
          {pending.map(task => {
            const criteria = parseCriteria(task.acceptance_criteria)
            const busy = busyId === task.id

            return (
              <section className="grid gap-2" key={task.id}>
                <div>
                  <p className="wrap-anywhere text-xs font-medium text-foreground/90">{task.goal}</p>
                  <p className="font-mono text-[0.65rem] text-muted-foreground/65">
                    {task.worker_name || task.worker_id} · {task.id}
                  </p>
                </div>
                {task.deliverable ? (
                  <div>
                    <p className="text-[0.6rem] font-medium uppercase tracking-wide text-muted-foreground/60">
                      {t.agents.deliverable}
                    </p>
                    <p className="whitespace-pre-wrap text-[0.72rem] leading-relaxed text-muted-foreground/85">
                      {task.deliverable}
                    </p>
                  </div>
                ) : null}
                {task.result ? (
                  <div>
                    <p className="text-[0.6rem] font-medium uppercase tracking-wide text-muted-foreground/60">
                      {copy.result}
                    </p>
                    <p className="max-h-48 overflow-y-auto whitespace-pre-wrap text-[0.72rem] leading-relaxed text-foreground/85">
                      {task.result}
                    </p>
                  </div>
                ) : null}
                {criteria.length > 0 ? (
                  <div>
                    <p className="text-[0.6rem] font-medium uppercase tracking-wide text-muted-foreground/60">
                      {t.agents.acceptanceCriteria}
                    </p>
                    {criteria.map((criterion, index) => (
                      <p className="text-[0.7rem] leading-relaxed text-muted-foreground/80" key={`${criterion}:${index}`}>
                        · {criterion}
                      </p>
                    ))}
                  </div>
                ) : null}
                <Textarea
                  aria-label={copy.feedback}
                  onChange={event => setFeedback(current => ({ ...current, [task.id]: event.target.value }))}
                  placeholder={copy.feedbackPlaceholder}
                  size="sm"
                  value={feedback[task.id] ?? ''}
                />
                <div className="flex justify-end gap-2">
                  <Button disabled={busy} onClick={() => void review(task, 'reject')} size="sm" variant="secondary">
                    {copy.reject}
                  </Button>
                  <Button disabled={busy} onClick={() => void review(task, 'approve')} size="sm">
                    {copy.approve}
                  </Button>
                </div>
              </section>
            )
          })}
        </div>
      </div>
    </div>
  )
}
