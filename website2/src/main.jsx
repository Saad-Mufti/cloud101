import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

console.log("wtf")
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <div>
      Bruh
    </div>
    {/* <App /> */}
  </StrictMode>,
)
