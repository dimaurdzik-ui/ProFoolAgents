import './Home.css'

import React from 'react'

export const Home: React.FC = () => {
  return (
    <div className="pixel-agents-home">
      <header className="home-header">
        <div className="hero-text">
          <h1>Welcome to Pixel Agents</h1>
          <p>Your intelligent workspace for autonomous multi-agent development.</p>
        </div>
      </header>

      <div className="dashboard-grid">
        <div className="glass-card">
          <div className="card-icon">📁</div>
          <h2>Recent Projects</h2>
          <p>Quickly jump back into your local workspaces.</p>
          <ul className="project-list">
            <li>
              frontend-redesign <span className="badge">Active</span>
            </li>
            <li>backend-api-v2</li>
            <li>landing-page</li>
          </ul>
          <button className="btn-secondary">Open Project</button>
        </div>

        <div className="glass-card">
          <div className="card-icon">🤖</div>
          <h2>Active Agents</h2>
          <p>Manage and monitor your running AI agents.</p>
          <div className="agent-status">
            <div className="text-sm text-muted-foreground p-3">
              Використовуйте каталог для додавання та керування агентами.
            </div>
          </div>
          <button className="btn-secondary">Create Agent</button>
        </div>

        <div className="glass-card">
          <div className="card-icon">⚡</div>
          <div className="flex-between">
            <h2>Provider Status</h2>
            <span className="status-badge ok">All Systems Go</span>
          </div>
          <p>Your API keys are securely loaded from the local OS Keychain.</p>
          <div className="stats-row">
            <div className="stat-box">
              <span className="stat-value">12.4k</span>
              <span className="stat-label">Tokens Today</span>
            </div>
            <div className="stat-box">
              <span className="stat-value">$0.14</span>
              <span className="stat-label">Est. Cost</span>
            </div>
          </div>
          <button className="btn-secondary">Manage Keys</button>
        </div>
      </div>
    </div>
  )
}
