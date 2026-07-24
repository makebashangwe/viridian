import './AppShell.css'

type AppShellProps = {
  children: React.ReactNode
}

function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <p className="app-brand">Viridian</p>
      </header>

      <main className="app-content">
        {children}
      </main>
    </div>
  )
}

export default AppShell