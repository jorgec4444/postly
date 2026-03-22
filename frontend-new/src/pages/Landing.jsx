import { useState } from "react"
import AuthModal from "../components/AuthModal"

function Landing() {
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsAuthModalOpen(true)}>
        Sign In
      </button>
      <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} />
    </div>
  )
}

export default Landing