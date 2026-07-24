import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router'
import { useAuth } from '../hooks/useAuth'

function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { signIn } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const destination =
    (
      location.state as {
        from?: {
          pathname?: string
        }
      } | null
    )?.from?.pathname ?? '/check-in'

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    setError('')
    setIsSubmitting(true)

    try {
      await signIn({
        email,
        password,
      })

      navigate(destination, { replace: true })
    } catch {
      setError('We could not log you in. Check your email and password.')
    } finally {
      setIsSubmitting(false)
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

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Logging in…' : 'Log in'}
        </button>
      </form>

      <p>New to Viridian? Create an account.</p>
    </section>
  )
}

export default LoginPage