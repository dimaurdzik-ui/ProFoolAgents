import React, { useState } from 'react'
import type { WorkerLive } from '../../store/workers'
import { useI18n } from '../../i18n'
import { Modal } from '../../components/ui/modal'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Textarea } from '../../components/ui/textarea'

interface AssignTaskModalProps {
  worker: WorkerLive
  onClose: () => void
  onSubmit: (task: any) => Promise<void>
}

export function AssignTaskModal({ worker, onClose, onSubmit }: AssignTaskModalProps) {
  const { t } = useI18n()
  const [goal, setGoal] = useState('')
  const [deliverable, setDeliverable] = useState('')
  const [priority, setPriority] = useState<'normal'|'high'|'low'|'urgent'>('normal')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (goal.length < 10) return
    setIsSubmitting(true)
    try {
      await onSubmit({
        worker_id: worker.worker_id,
        goal,
        deliverable,
        priority
      })
      onClose()
    } catch (err) {
      console.error(err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Modal title={t('agents.office.assignTask') || 'Assign Task'} onClose={onClose}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 p-4 min-w-[400px]">
        <div>
          <label className="text-sm font-medium mb-1 block">
            {t('agents.office.goal') || 'Goal'}
          </label>
          <Textarea 
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder={t('agents.office.goalPlaceholder') || 'What should this worker accomplish?'}
            minRows={3}
            required
          />
        </div>
        
        <div>
          <label className="text-sm font-medium mb-1 block">
            {t('agents.office.deliverable') || 'Expected deliverable'}
          </label>
          <Input 
            value={deliverable}
            onChange={(e) => setDeliverable(e.target.value)}
            placeholder={t('agents.office.deliverablePlaceholder') || 'What artifact should be produced?'}
          />
        </div>

        <div>
          <label className="text-sm font-medium mb-1 block">
            {t('agents.office.priority') || 'Priority'}
          </label>
          <select 
            className="w-full bg-base-800 border border-base-700 rounded p-2"
            value={priority}
            onChange={(e) => setPriority(e.target.value as any)}
          >
            <option value="low">{t('agents.office.priorityLow') || 'Low'}</option>
            <option value="normal">{t('agents.office.priorityNormal') || 'Normal'}</option>
            <option value="high">{t('agents.office.priorityHigh') || 'High'}</option>
            <option value="urgent">{t('agents.office.priorityUrgent') || 'Urgent'}</option>
          </select>
        </div>

        <div className="flex justify-end gap-2 mt-4">
          <Button variant="ghost" onClick={onClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button type="submit" disabled={isSubmitting || goal.length < 10}>
            {isSubmitting ? 'Assigning...' : 'Assign'}
          </Button>
        </div>
      </form>
    </Modal>
  )
}
