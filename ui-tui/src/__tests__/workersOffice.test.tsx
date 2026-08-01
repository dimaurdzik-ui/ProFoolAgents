import { describe, expect, it } from 'vitest'

import { renderToScreen } from '../../packages/pixel-agents-ink/src/ink/render-to-screen.js'
import { cellAtIndex, CellWidth, type Screen } from '../../packages/pixel-agents-ink/src/ink/screen.js'
import { getOverlayState, resetOverlayState } from '../app/overlayStore.js'
import { opsCommands } from '../app/slash/commands/ops.js'
import type { SlashRunCtx } from '../app/slash/types.js'
import { ReviewInbox } from '../components/workers/ReviewInbox.js'
import { StaffDirectory } from '../components/workers/StaffDirectory.js'

function screenText(screen: Screen): string {
  const lines: string[] = []

  for (let row = 0; row < screen.height; row += 1) {
    let line = ''

    for (let col = 0; col < screen.width; col += 1) {
      const cell = cellAtIndex(screen, row * screen.width + col)

      if (cell.width !== CellWidth.SpacerHead && cell.width !== CellWidth.SpacerTail) {
        line += cell.char
      }
    }

    lines.push(line.trimEnd())
  }

  return lines.join('\n')
}

describe('AI office TUI surface', () => {
  it('/team opens the persistent workers overlay', () => {
    resetOverlayState()
    const team = opsCommands.find(command => command.name === 'team')

    expect(team).toBeDefined()
    team?.run('', {} as SlashRunCtx, '/team')
    expect(getOverlayState().workers).toBe(true)
  })

  it('renders staff and review data returned by worker RPCs', () => {
    const staff = renderToScreen(
      <StaffDirectory
        selectedIndex={0}
        workers={[
          {
            autonomy_mode: 'smart',
            created_at: 1,
            display_name: 'SEO Specialist',
            status: 'idle',
            template_id: 'seo-specialist',
            worker_id: 'seo-1'
          }
        ]}
      />,
      100
    )

    const inbox = renderToScreen(
      <ReviewInbox
        onApprove={() => undefined}
        onReject={() => undefined}
        selectedIndex={0}
        tasks={[
          {
            created_at: 1,
            goal: 'Prepare launch audit',
            id: 'task-1',
            result: 'Audit complete',
            status: 'waiting_approval',
            worker_id: 'seo-1',
            worker_name: 'SEO Specialist'
          }
        ]}
      />,
      100
    )

    expect(screenText(staff.screen)).toContain('SEO Specialist')
    expect(screenText(inbox.screen)).toContain('Prepare launch audit')
    expect(screenText(inbox.screen)).toContain('Audit complete')
  })
})
