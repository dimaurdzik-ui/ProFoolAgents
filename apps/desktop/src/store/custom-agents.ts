import { atom } from 'nanostores'

// The draft's agent is only a default for the next session. Once a session
// exists, its agent identity is authoritative in the backend and is read via
// `session.agent`; keeping custom-agent records only in localStorage would
// create a UI option the agent runtime could never honour.
export const TEAM_AGENT_ID = 'pixel-team'

export const $selectedAgentId = atom<string>(TEAM_AGENT_ID)

// Catalog and selector are rendered in separate component subtrees.  Bump this
// after an install/uninstall so every `useAgents` instance re-reads backend
// truth instead of leaving the composer menu on a stale installed list.
export const $agentCatalogVersion = atom(0)

export function refreshAgentCatalog(): void {
  $agentCatalogVersion.set($agentCatalogVersion.get() + 1)
}
