import { Routes , Route } from 'react-router'
import AppShell from './layouts/AppShell'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import NotFoundPage from './pages/NotFoundPage'
import RegisterPage from './pages/RegisterPage'
import CheckInPage from './pages/CheckInPage'


function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/login" element={<LoginPage/>}/>
        <Route path="/register" element={<RegisterPage/>}/>
        <Route path="/check-in" element={<CheckInPage/>}/>
        <Route path="/*" element={<NotFoundPage/>}/>
      </Routes>
    </AppShell>
  )
}

export default App