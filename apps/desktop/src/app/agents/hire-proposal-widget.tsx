import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import type { OfficeHook, WorkerTask } from './office'
import { useState } from 'react'

export function HireProposalWidget({ 
  task, 
  office, 
  onReview 
}: { 
  task: WorkerTask, 
  office: OfficeHook,
  onReview: (task: WorkerTask, action: 'approve_hire' | 'reject_hire', feedback?: string) => Promise<void>
}) {
  const [feedback, setFeedback] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAction = async (action: 'approve_hire' | 'reject_hire') => {
    if (action === 'reject_hire' && !feedback.trim()) {
      setError('Please provide feedback/reason for rejection.')
      return
    }
    
    setBusy(true)
    setError(null)
    
    try {
      await onReview(task, action, feedback)
      setFeedback('')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="rounded-md border border-primary/50 bg-primary/10 p-4 grid gap-3 relative">
      {error && <p className="text-xs text-destructive">{error}</p>}
      
      <div className="flex items-center gap-2">
        <span className="text-[0.6rem] font-medium uppercase tracking-wide text-primary">
          Hire Request
        </span>
      </div>
      
      <div>
        <p className="text-sm font-medium">Role Requested: <span className="text-primary">{task.pending_hire_template_id}</span></p>
      </div>

      <div>
        <p className="text-[0.6rem] font-medium uppercase tracking-wide text-muted-foreground/60 mb-1">
          Reason
        </p>
        <p className="whitespace-pre-wrap text-[0.72rem] leading-relaxed text-foreground/85 bg-background p-2 rounded border border-border/50">
          {task.pending_hire_reason}
        </p>
      </div>

      <div>
        <p className="text-[0.6rem] font-medium uppercase tracking-wide text-muted-foreground/60 mb-1">
          Suggested Task
        </p>
        <p className="whitespace-pre-wrap text-[0.72rem] leading-relaxed text-foreground/85 bg-background p-2 rounded border border-border/50">
          {task.pending_hire_task}
        </p>
      </div>

      <Textarea
        placeholder="Optional feedback or rejection reason..."
        size="sm"
        value={feedback}
        onChange={e => setFeedback(e.target.value)}
        className="mt-2"
      />

      <div className="flex justify-end gap-2 mt-2">
        <Button 
          disabled={busy} 
          onClick={() => void handleAction('reject_hire')} 
          size="sm" 
          variant="secondary"
        >
          Reject Hire
        </Button>
        <Button 
          disabled={busy} 
          onClick={() => void handleAction('approve_hire')} 
          size="sm"
        >
          Approve & Hire
        </Button>
      </div>
    </div>
  )
}
