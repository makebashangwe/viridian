import { API_URL } from '../config/env'

export async function apiRequest(
  path: string,
  options?: RequestInit,
) {
  const token = sessionStorage.getItem('access_token')

  const headers = new Headers(options?.headers)

  if (!headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`)
  }

  return response
}