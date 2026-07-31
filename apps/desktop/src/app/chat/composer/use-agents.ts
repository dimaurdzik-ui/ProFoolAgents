import { useStore } from '@nanostores/react'
import { useCallback, useEffect, useState } from 'react'

import { useGatewayRequest } from '@/app/gateway/hooks/use-gateway-request'
import { $agentCatalogVersion, refreshAgentCatalog } from '@/store/custom-agents'

export type AgentTemplate = {
  id: string
  name: string
  category: string
  description: string
  capabilities?: string[]
  allowed_tools?: string[]
  starter_prompts?: string[]
}

type InstalledAgent = { id: string } | string

export function useAgents(sessionId?: string | null) {
  const { requestGateway } = useGatewayRequest()
  const catalogVersion = useStore($agentCatalogVersion)
  const [catalog, setCatalog] = useState<AgentTemplate[]>([])
  const [installed, setInstalled] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [sessionAgentId, setSessionAgentId] = useState<string>('general')

  const fetchAgents = useCallback(async () => {
    try {
      const [catRes, instRes] = await Promise.all([
        requestGateway<{ catalog: AgentTemplate[] }>('agents.catalog', {}),
        requestGateway<{ installed: InstalledAgent[] }>('agents.installed', {})
      ])

      if (catRes.catalog) {
        setCatalog(catRes.catalog)
      }

      if (instRes.installed) {
        setInstalled(
          instRes.installed
            .map(installedAgent => (typeof installedAgent === 'string' ? installedAgent : installedAgent.id))
            .filter(Boolean)
        )
      }
    } catch (e) {
      console.error('Failed to fetch agents:', e)
    } finally {
      setLoading(false)
    }
  }, [requestGateway])

  useEffect(() => {
    fetchAgents()
  }, [catalogVersion, fetchAgents])

  useEffect(() => {
    let cancelled = false

    if (!sessionId) {
      setSessionAgentId('general')

      return
    }

    void requestGateway<{ agent_id?: string | null }>('session.agent', { session_id: sessionId })
      .then(result => {
        if (!cancelled) {
          setSessionAgentId(result.agent_id || 'general')
        }
      })
      .catch(() => {
        if (!cancelled) {
          setSessionAgentId('general')
        }
      })

    return () => {
      cancelled = true
    }
  }, [requestGateway, sessionId])

  const install = async (agentId: string) => {
    await requestGateway('agents.install', { agent_id: agentId })
    await fetchAgents()
    refreshAgentCatalog()
  }

  const uninstall = async (agentId: string) => {
    await requestGateway('agents.uninstall', { agent_id: agentId })
    await fetchAgents()
    refreshAgentCatalog()
  }

  const setSessionAgent = async (sessionId: string, agentId: string | null) => {
    await requestGateway('session.set_agent', { session_id: sessionId, agent_id: agentId })
  }

  return { catalog, installed, loading, install, uninstall, fetchAgents, setSessionAgent, sessionAgentId }
}
