import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css' //index.css = applies global defaults using those values
import { BrowserRouter } from 'react-router'
import App from './App.tsx'

import './styles/tokens.css' //tokens.css = defines reusable design values

//component CSS = uses the same values repeatedly


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
    
  </StrictMode>,
)
