import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { toastConfig } from './config/toastConfig'
import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'
import AuthListener from './components/AuthListener'

function App() {
  return (
    <BrowserRouter>
    <Toaster {...toastConfig} />
    <AuthListener />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App