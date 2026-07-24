import { useNavigate } from 'react-router'
import type { ReactNode } from 'react'
import { useAuth } from '../hooks/useAuth'
import './AppShell.css'

type AppShellProps = {
  children: ReactNode
}

function AppShell({ children }: AppShellProps) {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    signOut()
    navigate('/login', { replace: true })
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <p className="app-brand">Viridian</p>

        {user && (
          <div>
            <span>{user.username}</span>
            <button type="button" onClick={handleLogout}>
              Log out
            </button>
          </div>
        )}
      </header>

      <main className="app-content">{children}</main>
    </div>
  )
}

export default AppShell