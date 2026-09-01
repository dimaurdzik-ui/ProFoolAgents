import { useMemo } from 'react'
import { OfficeHook, WorkerTask } from './office'
import { useI18n } from '@/i18n'
import { cn } from '@/lib/utils'

interface KanbanBoardProps {
  office: OfficeHook
}

const COLUMNS = [
  { id: 'todo', title: 'To Do', statuses: ['queued', 'pending'] },
  { id: 'in_progress', title: 'In Progress', statuses: ['working'] },
  { id: 'review', title: 'Review', statuses: ['waiting_approval', 'waiting_tool_approval', 'waiting_hire_approval'] },
  { id: 'done', title: 'Done', statuses: ['completed', 'failed', 'failed_permanently', 'rejected'] },
]

export function KanbanBoard({ office }: KanbanBoardProps) {
  const { t } = useI18n()
  
  const tasksByColumn = useMemo(() => {
    const result: Record<string, WorkerTask[]> = {
      todo: [],
      in_progress: [],
      review: [],
      done: [],
    }
    
    for (const task of office.data.tasks) {
      let placed = false
      for (const col of COLUMNS) {
        if (col.statuses.includes(task.status)) {
          result[col.id].push(task)
          placed = true
          break
        }
      }
      if (!placed) {
        result['todo'].push(task) // fallback
      }
    }
    
    return result
  }, [office.data.tasks])

  return (
    <div className="flex h-full gap-4 overflow-x-auto p-4">
      {COLUMNS.map((col) => (
        <div key={col.id} className="flex flex-col min-w-[280px] w-[280px] bg-secondary/10 rounded-lg p-3">
          <div className="flex items-center justify-between mb-3 px-1">
            <h3 className="font-semibold text-sm">{col.title}</h3>
            <span className="bg-secondary text-secondary-foreground text-xs rounded-full px-2 py-0.5">
              {tasksByColumn[col.id].length}
            </span>
          </div>
          <div className="flex flex-col gap-2 overflow-y-auto min-h-0 flex-1 overscroll-contain">
            {tasksByColumn[col.id].map((task) => (
              <TaskCard key={task.id} task={task} />
            ))}
            {tasksByColumn[col.id].length === 0 && (
              <div className="text-center p-4 border border-dashed rounded-lg border-border/50 text-muted-foreground/50 text-xs">
                No tasks
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

function TaskCard({ task }: { task: WorkerTask }) {
  return (
    <div className="bg-card text-card-foreground border rounded-lg p-3 shadow-sm flex flex-col gap-2 cursor-pointer hover:border-primary/50 transition-colors">
      <div className="flex justify-between items-start gap-2">
        <span className="text-xs font-mono text-muted-foreground truncate" title={task.id}>
          {task.id.split('-')[0]}
        </span>
        {task.priority && task.priority !== 'normal' && (
          <span className={cn(
            "text-[0.6rem] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded",
            task.priority === 'urgent' ? 'bg-destructive/20 text-destructive' :
            task.priority === 'high' ? 'bg-orange-500/20 text-orange-500' :
            'bg-secondary text-secondary-foreground'
          )}>
            {task.priority}
          </span>
        )}
      </div>
      <p className="text-sm font-medium line-clamp-3 leading-snug">{task.goal}</p>
      
      <div className="flex items-center justify-between mt-1 text-xs text-muted-foreground">
        <span className="flex items-center gap-1.5 truncate">
          <div className="w-4 h-4 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
            <span className="text-[0.5rem] font-bold text-primary">
              {task.worker_name ? task.worker_name.charAt(0).toUpperCase() : '?'}
            </span>
          </div>
          <span className="truncate">{task.worker_name || 'Unassigned'}</span>
        </span>
        
        {task.status === 'waiting_tool_approval' && (
          <span className="text-[0.65rem] text-primary bg-primary/10 px-1.5 py-0.5 rounded whitespace-nowrap">
            Tool wait
          </span>
        )}
        {task.status === 'failed' && (
          <span className="text-[0.65rem] text-destructive bg-destructive/10 px-1.5 py-0.5 rounded whitespace-nowrap">
            Failed
          </span>
        )}
      </div>
    </div>
  )
}
