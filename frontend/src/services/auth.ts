import { apiRequest } from './api'
import type {
  CurrentUser,
  LoginCredentials,
  RegistrationData,
  TokenResponse,
} from '../types/auth'

export async function register(
  registrationData: RegistrationData,
): Promise<CurrentUser> {
  const response = await apiRequest('/auth/register', {
    method: 'POST',
    body: JSON.stringify(registrationData),
  })

  return response.json()
}

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