export type LoginCredentials = {
  email: string
  password: string
}

export type RegistrationData = {
  email: string
  username: string
  password: string
}

export type TokenResponse = {
  access_token: string
  token_type: string
}

export type CurrentUser = {
  id: number
  email: string
  username: string
}