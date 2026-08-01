import { useState } from 'react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog'
import { Check, CheckCircle2 as ListIcon, Plus, Users, Wrench } from '@/lib/icons'
import { $selectedAgentId } from '@/store/custom-agents'

import { useAgents } from './use-agents'

export function AgentCreationDialog({
  open,
  onOpenChange,
  sessionId
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  sessionId: string | null
}) {
  const { catalog, installed, install, setSessionAgent } = useAgents()

  const handleInstall = async (agentId: string) => {
    await install(agentId)
    $selectedAgentId.set(agentId)

    if (sessionId) {
      await setSessionAgent(sessionId, agentId)
    }

    onOpenChange(false)
  }

  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('Усі')

  const categories = ['Усі', ...new Set(catalog.map(a => a.category))]

  const filteredCatalog = catalog.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(search.toLowerCase()) ||
                          agent.description.toLowerCase().includes(search.toLowerCase())
    const matchesCategory = selectedCategory === 'Усі' || agent.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  return (
    <Dialog onOpenChange={onOpenChange} open={open}>
      <DialogContent className="max-w-3xl gap-5 max-h-[85vh] flex flex-col">
        <DialogHeader>
          <DialogTitle icon={Users}>Каталог професійних агентів</DialogTitle>
          <DialogDescription>
            Оберіть помічника зі спеціалізованими інструментами та інструкціями для вашого завдання.
          </DialogDescription>
        </DialogHeader>

        <div className="flex gap-4 items-center">
          <input
            className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
            onChange={e => setSearch(e.target.value)}
            placeholder="Пошук працівників..."
            value={search}
          />
          <div className="flex gap-2 overflow-x-auto shrink-0 hide-scrollbar pb-1">
            {categories.map(cat => (
              <Button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                size="sm"
                variant={selectedCategory === cat ? 'default' : 'outline'}
                className="rounded-full text-xs"
              >
                {cat}
              </Button>
            ))}
          </div>
        </div>

        <div className="flex-1 overflow-y-auto grid md:grid-cols-2 gap-3 pr-2">
          {filteredCatalog.map(agent => (
            <div className="flex items-start justify-between p-3 border rounded-lg hover:border-primary/50 transition-colors" key={agent.id}>
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2">
                  <span className="font-semibold">{agent.name}</span>
                  <span className="text-[0.65rem] px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
                    {agent.category}
                  </span>
                </div>
                <span className="text-sm text-muted-foreground leading-snug">
                  {agent.description}
                </span>

                {agent.capabilities && agent.capabilities.length > 0 && (
                  <div className="mt-2 text-xs">
                    <div className="flex items-center gap-1.5 text-foreground/80 font-medium mb-1">
                      <ListIcon className="size-3" /> Основні можливості:
                    </div>
                    <ul className="list-disc pl-5 text-muted-foreground space-y-0.5">
                      {agent.capabilities.map((cap, i) => (
                        <li key={i}>{cap}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {agent.allowed_tools && agent.allowed_tools.length > 0 && (
                  <div className="mt-2 text-xs">
                    <div className="flex items-center gap-1.5 text-foreground/80 font-medium mb-1">
                      <Wrench className="size-3" /> Доступні інструменти:
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {agent.allowed_tools.map((tool, i) => (
                        <span className="px-1.5 py-0.5 bg-secondary/50 border rounded text-[10px] text-muted-foreground" key={i}>
                          {tool}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="pl-4 shrink-0">
                {installed.includes(agent.id) ? (
                  <Button className="gap-1.5 w-24" disabled size="sm" variant="outline">
                    <Check className="size-3.5" />
                    Додано
                  </Button>
                ) : (
                  <Button className="gap-1.5 w-24" onClick={() => handleInstall(agent.id)} size="sm">
                    <Plus className="size-3.5" />
                    Додати
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  )
}
