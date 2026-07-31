import { useStore } from '@nanostores/react'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import { Check, ChevronDown, Trash2, Users } from '@/lib/icons'
import { cn } from '@/lib/utils'
import { $selectedAgentId, TEAM_AGENT_ID } from '@/store/custom-agents'
import { requestFreshSession } from '@/store/profile'
import { $messagesEmpty } from '@/store/session'

import { useAgents } from './use-agents'

export function AgentSelector({
  disabled,
  sessionId,
  onOpenCreateDialog
}: {
  disabled?: boolean
  sessionId: string | null
  onOpenCreateDialog: () => void
}) {
  const { catalog, installed, uninstall, setSessionAgent, sessionAgentId } = useAgents(sessionId)

  // A draft uses the local selection; an existing chat is always rendered from
  // its backend-owned session metadata.
  const draftAgentId = useStore($selectedAgentId)
  const selectedAgentId = sessionId ? sessionAgentId : draftAgentId
  const messagesEmpty = useStore($messagesEmpty)
  const [open, setOpen] = useState(false)

  const [confirmDialog, setConfirmDialog] = useState<{ open: boolean; agentId: string | null; agentName: string }>({
    open: false,
    agentId: null,
    agentName: ''
  })

  const applySelection = async (agentId: string) => {
    $selectedAgentId.set(agentId)

    if (sessionId) {
      await setSessionAgent(sessionId, agentId === 'general' ? null : agentId)
    }
  }

  const handleSelect = async (agentId: string, agentName: string) => {
    if (!messagesEmpty && selectedAgentId !== agentId) {
      setConfirmDialog({ open: true, agentId, agentName })

      return
    }

    // A freshly created backend session may already be building its generic
    // agent. Start a new draft instead of racing that build; session.create
    // receives the selected agent id and builds the right identity first.
    if (sessionId && selectedAgentId !== agentId) {
      $selectedAgentId.set(agentId)
      requestFreshSession()

      return
    }

    await applySelection(agentId)
  }

  const handleConfirmNewChat = () => {
    if (confirmDialog.agentId) {
      $selectedAgentId.set(confirmDialog.agentId)
      requestFreshSession()
    }

    setConfirmDialog({ open: false, agentId: null, agentName: '' })
  }

  const generalAgent = {
    id: TEAM_AGENT_ID,
    name: 'Команда Pixel Agents',
    description: 'Оркестратор: залучає потрібних спеціалістів і об’єднує їхні результати'
  }

  const customAgents = catalog.filter(a => installed.includes(a.id))
  const agents = [generalAgent, ...customAgents]
  const selectedAgent = agents.find(a => a.id === selectedAgentId) || agents[0]

  return (
    <>
      <DropdownMenu onOpenChange={setOpen} open={open}>
        <DropdownMenuTrigger asChild>
          <Button
            aria-label="Вибір агента"
            className={cn(
              'h-(--composer-control-size) max-w-xs shrink-0 gap-1.5 rounded-md px-2 text-xs font-normal',
              'text-(--ui-text-tertiary) hover:bg-(--chrome-action-hover) hover:text-foreground'
            )}
            disabled={disabled}
            type="button"
            variant="ghost"
          >
            <Users className="size-3.5 shrink-0 opacity-70" />
            <span className="truncate">
              З ким спілкуєтесь:{' '}
              <span className="text-blue-600 dark:text-blue-400 font-medium">{selectedAgent?.name}</span>
            </span>
            <ChevronDown className="size-3.5 shrink-0 opacity-50" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" className="w-[300px] p-1" side="top" sideOffset={8}>
          <div className="px-2 py-1.5 text-[0.7rem] font-semibold tracking-wider text-muted-foreground uppercase">
            Доступні агенти
          </div>
          {agents.map(agent => (
            <DropdownMenuItem
              className="group flex cursor-pointer items-start gap-2.5 rounded-md px-2 py-1.5"
              key={agent.id}
              onClick={() => handleSelect(agent.id, agent.name)}
            >
              <div className="flex mt-0.5 h-4 w-4 shrink-0 items-center justify-center">
                {selectedAgentId === agent.id ? <Check className="size-3.5 text-blue-600 dark:text-blue-400" /> : null}
              </div>
              <div className="flex flex-col gap-0.5 min-w-0 flex-1">
                <span className="text-[0.8rem] font-medium leading-tight text-foreground/90 truncate">
                  {agent.name}
                </span>
                <span className="text-[0.7rem] leading-snug text-muted-foreground truncate">{agent.description}</span>
              </div>
              {agent.id !== TEAM_AGENT_ID && (
                <Button
                  className="opacity-0 group-hover:opacity-100 transition-opacity h-5 w-5 rounded-sm p-0 ml-1 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                  onClick={e => {
                    e.stopPropagation()
                    uninstall(agent.id)
                  }}
                  title="Видалити агента"
                  variant="ghost"
                >
                  <Trash2 className="size-3.5" />
                </Button>
              )}
            </DropdownMenuItem>
          ))}
          <DropdownMenuSeparator />
          <DropdownMenuItem
            className="flex cursor-pointer items-start gap-2.5 rounded-md px-2 py-1.5"
            onClick={() => {
              setOpen(false)
              onOpenCreateDialog()
            }}
          >
            <div className="flex mt-0.5 h-4 w-4 shrink-0 items-center justify-center" />
            <div className="flex flex-col gap-0.5">
              <span className="text-[0.8rem] font-medium leading-tight text-primary">+ Каталог агентів</span>
              <span className="text-[0.7rem] leading-snug text-muted-foreground">Додати професійного помічника</span>
            </div>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <Dialog
        onOpenChange={open => !open && setConfirmDialog({ open: false, agentId: null, agentName: '' })}
        open={confirmDialog.open}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Змінити співрозмовника?</DialogTitle>
            <DialogDescription>
              Поточна розмова належить агенту «{selectedAgent?.name}». Для спілкування з агентом «
              {confirmDialog.agentName}» буде створено новий чат.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button onClick={() => setConfirmDialog({ open: false, agentId: null, agentName: '' })} variant="outline">
              Скасувати
            </Button>
            <Button onClick={handleConfirmNewChat}>Створити новий чат</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}
