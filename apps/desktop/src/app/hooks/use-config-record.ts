import { useQuery } from '@tanstack/react-query'

import { queryClient, writeCache } from '@/lib/query-client'
import { getPixelAgentsConfigRecord } from '@/pixel-agents'
import type { PixelAgentsConfigRecord } from '@/types/pixel-agents'

// One shared cache for the whole profile config record (`GET /api/config`).
// Every settings surface (MCP, model, config) reads and writes through this key
// so a save in one shows in the others, and revisiting a tab paints the cache
// instead of blanking on a fresh fetch.
//
// Distinct from session/hooks/use-pixel-agents-config.ts, which is side-effecting —
// it pushes personality/cwd/voice/… into the session stores for live chat.
export const PIXEL_AGENTS_CONFIG_KEY = ['pixel-agents-config-record'] as const

// staleTime 0 → serve cache instantly, background-revalidate on every mount.
export const usePixelAgentsConfigRecord = () =>
  useQuery({ queryKey: PIXEL_AGENTS_CONFIG_KEY, queryFn: getPixelAgentsConfigRecord, staleTime: 0 })

export const setPixelAgentsConfigCache = writeCache<PixelAgentsConfigRecord>(PIXEL_AGENTS_CONFIG_KEY)

export const invalidatePixelAgentsConfig = () => queryClient.invalidateQueries({ queryKey: PIXEL_AGENTS_CONFIG_KEY })
