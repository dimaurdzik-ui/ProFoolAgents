import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { I18nProvider } from '@/i18n/context'

import { OfficeView } from './office'

const requestGateway = vi.fn()

vi.mock('@/app/gateway/hooks/use-gateway-request', () => ({
  useGatewayRequest: () => ({ requestGateway })
}))

function response(method: string) {
  if (method === 'workers.list') {
    return { workers: [] }
  }

  if (method === 'tasks.list') {
    return {
      tasks: [
        {
          acceptance_criteria: '["Includes a launch checklist"]',
          goal: 'Prepare launch audit',
          id: 'task-1',
          result: 'Audit complete',
          status: 'waiting_approval',
          worker_id: 'seo-1',
          worker_name: 'SEO Specialist'
        }
      ]
    }
  }

  if (method === 'agents.catalog') {
    return { catalog: [{ id: 'seo-specialist', name: 'SEO Specialist' }] }
  }

  return { success: true }
}

const renderOffice = (tab: 'review' | 'staff') =>
  render(
    <I18nProvider configClient={null} initialLocale="en">
      <OfficeView tab={tab} />
    </I18nProvider>
  )

describe('AI office desktop RPC wiring', () => {
  beforeEach(() => {
    requestGateway.mockImplementation(async (method: string) => response(method))
  })

  afterEach(() => {
    cleanup()
    vi.clearAllMocks()
  })

  it('hires a selected catalog role through workers.hire', async () => {
    renderOffice('staff')

    const hire = await screen.findByRole('button', { name: 'Hire worker' })
    await waitFor(() => expect(hire.hasAttribute('disabled')).toBe(false))
    fireEvent.click(hire)

    await waitFor(() =>
      expect(requestGateway).toHaveBeenCalledWith(
        'workers.hire',
        expect.objectContaining({ autonomy_mode: 'smart', template_id: 'seo-specialist' })
      )
    )
  })

  it('rejects reviewed work with required feedback', async () => {
    renderOffice('review')

    expect(await screen.findByText('Prepare launch audit')).toBeTruthy()
    fireEvent.change(screen.getByLabelText('Review feedback'), { target: { value: 'Add competitor evidence' } })
    fireEvent.click(screen.getByRole('button', { name: 'Reject and retry' }))

    await waitFor(() =>
      expect(requestGateway).toHaveBeenCalledWith('tasks.reject', {
        feedback: 'Add competitor evidence',
        task_id: 'task-1'
      })
    )
  })
})
