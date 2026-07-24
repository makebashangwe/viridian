import { useState } from 'react'
import { useNavigate } from 'react-router'
import { getCurrentUser, login } from '../services/auth'

function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const navigate = useNavigate()

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    setError('')
    setIsLoading(true)

    try {
      const token = await login({
        email,
        password,
      })

      sessionStorage.setItem('access_token', token.access_token)

      await getCurrentUser()

      navigate('/check-in')
    } catch {
      sessionStorage.removeItem('access_token')
      setError('We could not log you in. Check your email and password.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section>
      <h1>Log In</h1>
      <p>Access your check-ins and continue where you left off.</p>

      {error && <p role="alert">{error}</p>}

      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in…' : 'Log in'}
        </button>
      </form>

      <p>New to Viridian? Create an account.</p>
    </section>
  )
}

export default LoginPage