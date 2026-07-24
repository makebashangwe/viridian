import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { AuthContext } from './auth-context'
import { getCurrentUser, login } from '../services/auth'
import type { CurrentUser, LoginCredentials } from '../types/auth'

type AuthProviderProps = {
  children: ReactNode
}

function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function restoreSession() {
      const token = sessionStorage.getItem('access_token')

      if (!token) {
        setIsLoading(false)
        return
      }

      try {
        const currentUser = await getCurrentUser()
        setUser(currentUser)
      } catch {
        sessionStorage.removeItem('access_token')
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    void restoreSession()
  }, [])

  async function signIn(credentials: LoginCredentials) {
    const token = await login(credentials)

    sessionStorage.setItem('access_token', token.access_token)

    try {
      const currentUser = await getCurrentUser()
      setUser(currentUser)
    } catch (error) {
      sessionStorage.removeItem('access_token')
      setUser(null)
      throw error
    }
  }

  function signOut() {
    sessionStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        signIn,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider