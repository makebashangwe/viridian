import { createContext } from 'react'
import type { LoginCredentials, CurrentUser } from '../types/auth'

export type AuthContextValue = {
  user: CurrentUser | null
  isLoading: boolean
  signIn: (credentials: LoginCredentials) => Promise<void>
  signOut: () => void
}

export const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
)