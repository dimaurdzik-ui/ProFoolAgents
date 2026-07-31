import { contextBridge, ipcRenderer, webUtils } from 'electron'

contextBridge.exposeInMainWorld('pixelAgentsDesktop', {
  getConnection: profile => ipcRenderer.invoke('pixel-agents:connection', profile),
  revalidateConnection: () => ipcRenderer.invoke('pixel-agents:connection:revalidate'),
  touchBackend: profile => ipcRenderer.invoke('pixel-agents:backend:touch', profile),
  getGatewayWsUrl: profile => ipcRenderer.invoke('pixel-agents:gateway:ws-url', profile),
  openSessionWindow: (sessionId, opts) => ipcRenderer.invoke('pixel-agents:window:openSession', sessionId, opts),
  openWindow: () => ipcRenderer.invoke('pixel-agents:window:openInstance'),
  claimAmbientCue: key => ipcRenderer.invoke('pixel-agents:ambient:claim', key),
  petOverlay: {
    // Main renderer → main process: window lifecycle + drag. `request` is
    // `{ bounds, screen }`; resolves with the screen bounds it actually used.
    open: request => ipcRenderer.invoke('pixel-agents:pet-overlay:open', request),
    close: () => ipcRenderer.invoke('pixel-agents:pet-overlay:close'),
    setBounds: bounds => ipcRenderer.send('pixel-agents:pet-overlay:set-bounds', bounds),
    setIgnoreMouse: ignore => ipcRenderer.send('pixel-agents:pet-overlay:ignore-mouse', ignore),
    // Flip the overlay focusable (and focus it) while the composer needs keys.
    setFocusable: focusable => ipcRenderer.send('pixel-agents:pet-overlay:set-focusable', focusable),
    // Main renderer → overlay (forwarded by main): push the latest pet state.
    pushState: payload => ipcRenderer.send('pixel-agents:pet-overlay:state', payload),
    // Overlay → main renderer (forwarded by main): pop back in / composer submit.
    control: payload => ipcRenderer.send('pixel-agents:pet-overlay:control', payload),
    // Overlay subscribes to state pushes.
    onState: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('pixel-agents:pet-overlay:state', listener)

      return () => ipcRenderer.removeListener('pixel-agents:pet-overlay:state', listener)
    },
    // Main renderer subscribes to overlay control messages.
    onControl: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('pixel-agents:pet-overlay:control', listener)

      return () => ipcRenderer.removeListener('pixel-agents:pet-overlay:control', listener)
    }
  },
  // Quick Entry: the global-hotkey mini composer window. Main owns the OS
  // shortcut + the persisted preference; the quick window only captures text
  // and hands it back, and the primary renderer submits it through the normal
  // prompt path.
  quickEntry: {
    getSettings: () => ipcRenderer.invoke('pixel-agents:quick-entry:settings:get'),
    setSettings: patch => ipcRenderer.invoke('pixel-agents:quick-entry:settings:set', patch),
    submit: payload => ipcRenderer.send('pixel-agents:quick-entry:submit', payload),
    dismiss: () => ipcRenderer.send('pixel-agents:quick-entry:dismiss'),
    // Primary renderer → main → quick window: gateway connection state + the
    // recent-session options the target picker offers. Main caches the latest
    // payload so a freshly spawned quick window starts from truth.
    pushState: payload => ipcRenderer.send('pixel-agents:quick-entry:state', payload),
    // Quick window subscribes to those pushes.
    onState: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('pixel-agents:quick-entry:state', listener)

      return () => ipcRenderer.removeListener('pixel-agents:quick-entry:state', listener)
    },
    // Main → primary renderer: a submit captured by the quick window.
    onSubmit: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('pixel-agents:quick-entry:submit', listener)

      return () => ipcRenderer.removeListener('pixel-agents:quick-entry:submit', listener)
    },
    // Main → quick window: you were just summoned (reset draft + refocus).
    onShown: callback => {
      const listener = () => callback()
      ipcRenderer.on('pixel-agents:quick-entry:shown', listener)

      return () => ipcRenderer.removeListener('pixel-agents:quick-entry:shown', listener)
    }
  },
  getBootProgress: () => ipcRenderer.invoke('pixel-agents:boot-progress:get'),
  getConnectionConfig: profile => ipcRenderer.invoke('pixel-agents:connection-config:get', profile),
  saveConnectionConfig: payload => ipcRenderer.invoke('pixel-agents:connection-config:save', payload),
  applyConnectionConfig: payload => ipcRenderer.invoke('pixel-agents:connection-config:apply', payload),
  testConnectionConfig: payload => ipcRenderer.invoke('pixel-agents:connection-config:test', payload),
  sshConfigHosts: () => ipcRenderer.invoke('pixel-agents:ssh-config:hosts'),
  sshResolveHost: host => ipcRenderer.invoke('pixel-agents:ssh-config:resolve', host),
  probeConnectionConfig: remoteUrl => ipcRenderer.invoke('pixel-agents:connection-config:probe', remoteUrl),
  oauthLoginConnectionConfig: remoteUrl => ipcRenderer.invoke('pixel-agents:connection-config:oauth-login', remoteUrl),
  oauthLogoutConnectionConfig: remoteUrl =>
    ipcRenderer.invoke('pixel-agents:connection-config:oauth-logout', remoteUrl),
  // Pixel Agents Cloud: one portal login powers discovery + silent per-agent sign-in
  // (cloud-auto-discovery Phase 3).
  cloud: {
    status: () => ipcRenderer.invoke('pixel-agents:cloud:status'),
    login: () => ipcRenderer.invoke('pixel-agents:cloud:login'),
    logout: () => ipcRenderer.invoke('pixel-agents:cloud:logout'),
    discover: org => ipcRenderer.invoke('pixel-agents:cloud:discover', org),
    agentSignIn: dashboardUrl => ipcRenderer.invoke('pixel-agents:cloud:agent-sign-in', dashboardUrl)
  },
  profile: {
    get: () => ipcRenderer.invoke('pixel-agents:profile:get'),
    set: name => ipcRenderer.invoke('pixel-agents:profile:set', name)
  },
  api: request => ipcRenderer.invoke('pixel-agents:api', request),
  notify: payload => ipcRenderer.invoke('pixel-agents:notify', payload),
  requestMicrophoneAccess: () => ipcRenderer.invoke('pixel-agents:requestMicrophoneAccess'),
  readFileDataUrl: filePath => ipcRenderer.invoke('pixel-agents:readFileDataUrl', filePath),
  readFileDataUrlForAttach: filePath => ipcRenderer.invoke('pixel-agents:readFileDataUrlForAttach', filePath),
  dataUrlReadMax: {
    get: () => ipcRenderer.invoke('pixel-agents:data-url-read-max:get'),
    set: maxMb => ipcRenderer.invoke('pixel-agents:data-url-read-max:set', maxMb)
  },
  readFileText: filePath => ipcRenderer.invoke('pixel-agents:readFileText', filePath),
  selectPaths: options => ipcRenderer.invoke('pixel-agents:selectPaths', options),
  writeClipboard: text => ipcRenderer.invoke('pixel-agents:writeClipboard', text),
  readClipboard: () => ipcRenderer.invoke('pixel-agents:readClipboard'),
  saveImageFromUrl: url => ipcRenderer.invoke('pixel-agents:saveImageFromUrl', url),
  saveImageBuffer: (data, ext) => ipcRenderer.invoke('pixel-agents:saveImageBuffer', { data, ext }),
  saveClipboardImage: () => ipcRenderer.invoke('pixel-agents:saveClipboardImage'),
  getPathForFile: file => {
    try {
      return webUtils.getPathForFile(file) || ''
    } catch {
      return ''
    }
  },
  normalizePreviewTarget: (target, baseDir) =>
    ipcRenderer.invoke('pixel-agents:normalizePreviewTarget', target, baseDir),
  watchPreviewFile: url => ipcRenderer.invoke('pixel-agents:watchPreviewFile', url),
  watchDirectory: dir => ipcRenderer.invoke('pixel-agents:watchDirectory', dir),
  stopPreviewFileWatch: id => ipcRenderer.invoke('pixel-agents:stopPreviewFileWatch', id),
  setActiveWork: payload => ipcRenderer.send('pixel-agents:active-work', payload),
  setTitleBarTheme: payload => ipcRenderer.send('pixel-agents:titlebar-theme', payload),
  setNativeTheme: mode => ipcRenderer.send('pixel-agents:native-theme', mode),
  setTranslucency: payload => ipcRenderer.send('pixel-agents:translucency', payload),
  setKeepAwake: on => ipcRenderer.send('pixel-agents:keep-awake', on),
  setPreviewShortcutActive: active => ipcRenderer.send('pixel-agents:previewShortcutActive', Boolean(active)),
  openExternal: url => ipcRenderer.invoke('pixel-agents:openExternal', url),
  openPreviewInBrowser: url => ipcRenderer.invoke('pixel-agents:openPreviewInBrowser', url),
  fetchLinkTitle: url => ipcRenderer.invoke('pixel-agents:fetchLinkTitle', url),
  sanitizeWorkspaceCwd: cwd => ipcRenderer.invoke('pixel-agents:workspace:sanitize', cwd),
  settings: {
    getDefaultProjectDir: () => ipcRenderer.invoke('pixel-agents:setting:defaultProjectDir:get'),
    setDefaultProjectDir: dir => ipcRenderer.invoke('pixel-agents:setting:defaultProjectDir:set', dir),
    pickDefaultProjectDir: () => ipcRenderer.invoke('pixel-agents:setting:defaultProjectDir:pick')
  },
  zoom: {
    // Current zoom of this window, as { level, percent }.
    get: () => ipcRenderer.invoke('pixel-agents:zoom:get'),
    setPercent: percent => ipcRenderer.send('pixel-agents:zoom:set-percent', percent),
    // Fires on every zoom change, including the Ctrl/Cmd +/-/0 shortcuts,
    // so the settings UI can stay in sync with the keyboard.
    onChanged: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('pixel-agents:zoom:changed', listener)

      return () => ipcRenderer.removeListener('pixel-agents:zoom:changed', listener)
    }
  },
  revealLogs: () => ipcRenderer.invoke('pixel-agents:logs:reveal'),
  getRecentLogs: () => ipcRenderer.invoke('pixel-agents:logs:recent'),
  readDir: dirPath => ipcRenderer.invoke('pixel-agents:fs:readDir', dirPath),
  gitRoot: startPath => ipcRenderer.invoke('pixel-agents:fs:gitRoot', startPath),
  revealPath: targetPath => ipcRenderer.invoke('pixel-agents:fs:reveal', targetPath),
  openDir: dirPath => ipcRenderer.invoke('pixel-agents:fs:openDir', dirPath),
  desktopPluginsRoot: () => ipcRenderer.invoke('pixel-agents:fs:desktopPluginsRoot'),
  renamePath: (targetPath, newName) => ipcRenderer.invoke('pixel-agents:fs:rename', targetPath, newName),
  writeTextFile: (filePath, content) => ipcRenderer.invoke('pixel-agents:fs:writeText', filePath, content),
  trashPath: targetPath => ipcRenderer.invoke('pixel-agents:fs:trash', targetPath),
  git: {
    worktreeList: repoPath => ipcRenderer.invoke('pixel-agents:git:worktreeList', repoPath),
    worktreeAdd: (repoPath, options) => ipcRenderer.invoke('pixel-agents:git:worktreeAdd', repoPath, options),
    worktreeRemove: (repoPath, worktreePath, options) =>
      ipcRenderer.invoke('pixel-agents:git:worktreeRemove', repoPath, worktreePath, options),
    branchSwitch: (repoPath, branch) => ipcRenderer.invoke('pixel-agents:git:branchSwitch', repoPath, branch),
    branchList: repoPath => ipcRenderer.invoke('pixel-agents:git:branchList', repoPath),
    baseBranchList: repoPath => ipcRenderer.invoke('pixel-agents:git:baseBranchList', repoPath),
    repoStatus: repoPath => ipcRenderer.invoke('pixel-agents:git:repoStatus', repoPath),
    fileDiff: (repoPath, filePath) => ipcRenderer.invoke('pixel-agents:git:fileDiff', repoPath, filePath),
    scanRepos: (roots, options) => ipcRenderer.invoke('pixel-agents:git:scanRepos', roots, options),
    review: {
      list: (repoPath, scope, baseRef) => ipcRenderer.invoke('pixel-agents:git:review:list', repoPath, scope, baseRef),
      diff: (repoPath, filePath, scope, baseRef, staged) =>
        ipcRenderer.invoke('pixel-agents:git:review:diff', repoPath, filePath, scope, baseRef, staged),
      stage: (repoPath, filePath) => ipcRenderer.invoke('pixel-agents:git:review:stage', repoPath, filePath),
      unstage: (repoPath, filePath) => ipcRenderer.invoke('pixel-agents:git:review:unstage', repoPath, filePath),
      revert: (repoPath, filePath) => ipcRenderer.invoke('pixel-agents:git:review:revert', repoPath, filePath),
      revParse: (repoPath, ref) => ipcRenderer.invoke('pixel-agents:git:review:revParse', repoPath, ref),
      commit: (repoPath, message, push) =>
        ipcRenderer.invoke('pixel-agents:git:review:commit', repoPath, message, push),
      commitContext: repoPath => ipcRenderer.invoke('pixel-agents:git:review:commitContext', repoPath),
      push: repoPath => ipcRenderer.invoke('pixel-agents:git:review:push', repoPath),
      shipInfo: repoPath => ipcRenderer.invoke('pixel-agents:git:review:shipInfo', repoPath),
      createPr: repoPath => ipcRenderer.invoke('pixel-agents:git:review:createPr', repoPath)
    }
  },
  terminal: {
    cwd: id => ipcRenderer.invoke('pixel-agents:terminal:cwd', id),
    dispose: id => ipcRenderer.invoke('pixel-agents:terminal:dispose', id),
    resize: (id, size) => ipcRenderer.invoke('pixel-agents:terminal:resize', id, size),
    start: options => ipcRenderer.invoke('pixel-agents:terminal:start', options),
    write: (id, data) => ipcRenderer.invoke('pixel-agents:terminal:write', id, data),
    onData: (id, callback) => {
      const channel = `pixel-agents:terminal:${id}:data`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)

      return () => ipcRenderer.removeListener(channel, listener)
    },
    onExit: (id, callback) => {
      const channel = `pixel-agents:terminal:${id}:exit`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)

      return () => ipcRenderer.removeListener(channel, listener)
    }
  },
  onClosePreviewRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('pixel-agents:close-preview-requested', listener)

    return () => ipcRenderer.removeListener('pixel-agents:close-preview-requested', listener)
  },
  onOpenFolderRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('pixel-agents:open-folder-requested', listener)

    return () => ipcRenderer.removeListener('pixel-agents:open-folder-requested', listener)
  },
  onOpenUpdatesRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('pixel-agents:open-updates', listener)

    return () => ipcRenderer.removeListener('pixel-agents:open-updates', listener)
  },
  onDeepLink: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('pixel-agents:deep-link', listener)

    return () => ipcRenderer.removeListener('pixel-agents:deep-link', listener)
  },
  signalDeepLinkReady: () => ipcRenderer.invoke('pixel-agents:deep-link-ready'),
  onWindowStateChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('pixel-agents:window-state-changed', listener)

    return () => ipcRenderer.removeListener('pixel-agents:window-state-changed', listener)
  },
  onFocusSession: callback => {
    const listener = (_event, sessionId) => callback(sessionId)
    ipcRenderer.on('pixel-agents:focus-session', listener)

    return () => ipcRenderer.removeListener('pixel-agents:focus-session', listener)
  },
  onNotificationAction: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('pixel-agents:notification-action', listener)

    return () => ipcRenderer.removeListener('pixel-agents:notification-action', listener)
  },
  onPreviewFileChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('pixel-agents:preview-file-changed', listener)

    return () => ipcRenderer.removeListener('pixel-agents:preview-file-changed', listener)
  },
  onBackendExit: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('pixel-agents:backend-exit', listener)

    return () => ipcRenderer.removeListener('pixel-agents:backend-exit', listener)
  },
  // Soft gateway-mode apply finished tearing down the primary backend. Renderer
  // should wipe session lists + re-dial without a window reload.
  onConnectionApplied: callback => {
    const listener = () => callback()
    ipcRenderer.on('pixel-agents:connection:applied', listener)

    return () => ipcRenderer.removeListener('pixel-agents:connection:applied', listener)
  },
  onPowerResume: callback => {
    const listener = () => callback()
    ipcRenderer.on('pixel-agents:power-resume', listener)

    return () => ipcRenderer.removeListener('pixel-agents:power-resume', listener)
  },
  onBootProgress: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('pixel-agents:boot-progress', listener)

    return () => ipcRenderer.removeListener('pixel-agents:boot-progress', listener)
  },
  // First-launch bootstrap progress -- emitted by the install.ps1 stage
  // runner in main.ts (apps/desktop/electron/bootstrap-runner.ts).
  // Renderer's install overlay subscribes to live events and queries the
  // current snapshot via getBootstrapState() to recover after a devtools
  // reload mid-bootstrap.
  getBootstrapState: () => ipcRenderer.invoke('pixel-agents:bootstrap:get'),
  continueBootstrapLocal: () => ipcRenderer.invoke('pixel-agents:bootstrap:continue-local'),
  resetBootstrap: () => ipcRenderer.invoke('pixel-agents:bootstrap:reset'),
  repairBootstrap: () => ipcRenderer.invoke('pixel-agents:bootstrap:repair'),
  cancelBootstrap: () => ipcRenderer.invoke('pixel-agents:bootstrap:cancel'),
  onBootstrapEvent: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('pixel-agents:bootstrap:event', listener)

    return () => ipcRenderer.removeListener('pixel-agents:bootstrap:event', listener)
  },
  getVersion: () => ipcRenderer.invoke('pixel-agents:version'),
  getRemoteDisplayReason: () => ipcRenderer.invoke('pixel-agents:get-remote-display-reason'),
  uninstall: {
    summary: () => ipcRenderer.invoke('pixel-agents:uninstall:summary'),
    run: mode => ipcRenderer.invoke('pixel-agents:uninstall:run', { mode })
  },
  updates: {
    check: () => ipcRenderer.invoke('pixel-agents:updates:check'),
    apply: opts => ipcRenderer.invoke('pixel-agents:updates:apply', opts),
    getBranch: () => ipcRenderer.invoke('pixel-agents:updates:branch:get'),
    setBranch: name => ipcRenderer.invoke('pixel-agents:updates:branch:set', name),
    onProgress: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('pixel-agents:updates:progress', listener)

      return () => ipcRenderer.removeListener('pixel-agents:updates:progress', listener)
    }
  },
  themes: {
    fetchMarketplace: id => ipcRenderer.invoke('pixel-agents:vscode-theme:fetch', id),
    searchMarketplace: query => ipcRenderer.invoke('pixel-agents:vscode-theme:search', query)
  },
  // Find-in-page (Ctrl/Cmd+F): delegates to Electron's
  // webContents.findInPage on the IPC sender's window so a Cmd+F pressed
  // in a secondary session window searches THAT window, not the primary.
  // `onFoundInPage` returns the unsubscribe fn; the renderer wires it via
  // `initFindInPageListener` in store/find-in-page.ts and tears it down
  // when the FindBar unmounts.
  findInPage: (query, options) => ipcRenderer.invoke('pixel-agents:find-in-page', query, options),
  stopFindInPage: () => ipcRenderer.invoke('pixel-agents:stop-find-in-page'),
  onFoundInPage: callback => {
    const listener = (_event, result) => callback(result)
    ipcRenderer.on('pixel-agents:found-in-page', listener)

    return () => ipcRenderer.removeListener('pixel-agents:found-in-page', listener)
  }
})
