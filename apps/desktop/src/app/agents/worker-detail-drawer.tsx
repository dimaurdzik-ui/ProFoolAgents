import React, { useState } from 'react'
import type { WorkerLive, WorkerTask } from '../../store/workers'
import { useI18n } from '../../i18n'
import { Drawer } from '../../components/ui/drawer'
import { Button } from '../../components/ui/button'

interface WorkerDetailDrawerProps {
  worker: WorkerLive
  tasks: WorkerTask[]
  onClose: () => void
  onAssignTask: (worker: WorkerLive) => void
}

export function WorkerDetailDrawer({ worker, tasks, onClose, onAssignTask }: WorkerDetailDrawerProps) {
  const { t } = useI18n()
  const [activeTab, setActiveTab] = useState<'active'|'history'>('active')

  const activeTasks = tasks.filter(t => t.status === 'working' || t.status === 'queued')
  const historyTasks = tasks.filter(t => !['working', 'queued'].includes(t.status))

  return (
    <Drawer onClose={onClose} position="right" className="w-[500px] flex flex-col">
      <div className="p-4 border-b border-base-800 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold">{worker.display_name}</h2>
          <div className="text-sm text-base-400">Template: {worker.template_id} • Status: {worker.status}</div>
        </div>
        <Button onClick={() => onAssignTask(worker)} size="sm">
          {t('agents.office.assignTask') || 'Assign Task'}
        </Button>
      </div>
      
      <div className="flex border-b border-base-800 px-4">
        <button 
          className={`py-2 px-4 ${activeTab === 'active' ? 'border-b-2 border-primary-500 text-primary-500' : 'text-base-400'}`}
          onClick={() => setActiveTab('active')}
        >
          {t('agents.office.activeTask') || 'Active Task'} ({activeTasks.length})
        </button>
        <button 
          className={`py-2 px-4 ${activeTab === 'history' ? 'border-b-2 border-primary-500 text-primary-500' : 'text-base-400'}`}
          onClick={() => setActiveTab('history')}
        >
          {t('agents.office.taskHistory') || 'Task History'} ({historyTasks.length})
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {activeTab === 'active' && (
          <div className="flex flex-col gap-4">
            {activeTasks.length === 0 ? (
              <div className="text-base-400 text-center py-8">{t('agents.office.noActiveTask') || 'No active task'}</div>
            ) : (
              activeTasks.map(task => (
                <div key={task.id} className="bg-base-900 border border-base-800 p-4 rounded-lg">
                  <div className="font-medium">{task.goal}</div>
                  <div className="text-sm text-base-400 mt-2">Priority: {task.priority}</div>
                  <div className="text-sm text-primary-400 mt-1">Status: {task.status}</div>
                </div>
              ))
            )}
          </div>
        )}
        
        {activeTab === 'history' && (
          <div className="flex flex-col gap-4">
            {historyTasks.map(task => (
              <div key={task.id} className="bg-base-900 border border-base-800 p-4 rounded-lg opacity-80">
                <div className="font-medium">{task.goal}</div>
                <div className="text-sm text-base-400 mt-2">Status: {task.status}</div>
                {task.result && <div className="mt-2 text-sm bg-base-800 p-2 rounded max-h-32 overflow-y-auto">{task.result}</div>}
              </div>
            ))}
          </div>
        )}
      </div>
    </Drawer>
  )
}
