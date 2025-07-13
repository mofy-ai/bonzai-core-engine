// 💜 MAMA BEAR'S MAIN REACT ENTRY POINT - STARTING THE FAMILY! 🚀
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// 💜 Create our beautiful family home!
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
