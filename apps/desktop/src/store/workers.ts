import { atom } from 'nanostores'

export interface SubagentStreamEntry {
  type: string
  payload?: any
}

export interface WorkerLive {
  worker_id: string
  display_name: string
  template_id: string
  autonomy_mode: 'autonomous' | 'manual' | 'smart'
  status: 'error' | 'idle' | 'paused' | 'working' | 'onboarding'
  manager_id?: null | string
  current_task_id?: string
  progress?: SubagentStreamEntry[]
}

export interface WorkerTask {
  id: string
  worker_id: string
  worker_name?: string
  goal: string
  deliverable?: string
  acceptance_criteria?: string
  priority: 'high' | 'low' | 'normal' | 'urgent'
  deadline_at?: number
  status: 'approved' | 'completed' | 'done' | 'failed' | 'failed_permanently' | 'queued' | 'rejected' | 'waiting_approval' | 'waiting_hire_approval' | 'waiting_tool_approval' | 'working'
  result?: string
  last_error?: string
  retry_count: number
  max_retries: number
  created_at: number
  updated_at: number
  pending_tool_name?: string
  pending_tool_args?: string
  pending_hire_template_id?: string
  pending_hire_reason?: string
  pending_hire_task?: string
}

export const $workers = atom<WorkerLive[]>([])
export const $workerTasks = atom<Record<string, WorkerTask[]>>({})

// Persistent UI state for Office view
export const $officeActiveTab = atom<import('../app/agents/office').OfficeTab>('live')
export const $officeSelectedWorkerId = atom<string | null>(null)

export const activeWorkers = (workers: WorkerLive[]) =>
  workers.filter(w => w.status === 'working')
