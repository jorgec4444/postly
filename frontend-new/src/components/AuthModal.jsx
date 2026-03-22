import { supabase } from "../supabase"

async function signInWithGoogle() {
    const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
            redirectTo: window.location.origin + '/dashboard',
        }
    })
    if (error) {
        console.error('Error signing in with Google:', error.message)
    }
}
function AuthModal({ isOpen, onClose }) {
  if (!isOpen) return null

  return (
    <div>
      <h2>Sign in to Orkly</h2>
      <button onClick={signInWithGoogle}>
        Sign in with Google
      </button>
      <button onClick={onClose}>
        Close
      </button>
    </div>
  )
}

export default AuthModal