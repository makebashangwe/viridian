import { apiRequest } from './api'
import type {
  CurrentUser,
  LoginCredentials,
  TokenResponse,
} from '../types/auth'

export async function login(
  credentials: LoginCredentials,
): Promise<TokenResponse> {
  const response = await apiRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  })

  return response.json()
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await apiRequest('/auth/me')
  return response.json()
}