import { useEffect, useState } from "react";
import { X } from "lucide-react";
import { supabase } from "../supabase";
import { useTranslation } from "react-i18next";

async function signInWithGoogle() {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: "google",
    options: {
      redirectTo: window.location.origin + "/dashboard",
    },
  });
  if (error) console.error("Error signing in with Google:", error.message);
}

export default function AuthModal({ isOpen, onClose }) {
  const { t } = useTranslation();
  const [mode, setMode] = useState("login"); // "login" | "register" | "magic"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [magicSent, setMagicSent] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    const handleKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [isOpen, onClose]);

  // Reset al cerrar
  useEffect(() => {
    if (!isOpen) {
      setEmail("");
      setPassword("");
      setError(null);
      setMagicSent(false);
      setMode("login");
    }
  }, [isOpen]);

  const handleEmailAuth = async () => {
    if (!email.trim() || !password.trim()) return;
    setLoading(true);
    setError(null);
    try {
      if (mode === "register") {
        const { error } = await supabase.auth.signUp({ email, password });
        if (error) throw error;
      } else {
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
      }
      onClose();
      window.location.href = "/dashboard";
    } catch (e) {
      if (e.message.includes("Invalid login credentials")) {
        setError(t('auth.errorInvalidCredentials'));
      } else if (e.message.includes("already registered") || e.message.includes("already been registered")) {
        setError(t('auth.errorEmailTaken'));
      } else {
        setError(t('auth.errorGeneric'));
      }
    } finally {
      setLoading(false);
    }
  };

  const handleMagicLink = async () => {
    if (!email.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const { error } = await supabase.auth.signInWithOtp({
        email,
        options: { emailRedirectTo: window.location.origin + "/dashboard" },
      });
      if (error) throw error;
      setMagicSent(true);
    } catch (e) {
      setError(t('auth.errorGeneric'));
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-white border border-gray-200 rounded-2xl shadow-2xl w-full max-w-sm mx-4 overflow-hidden">

        {/* Top accent bar */}
        <div className="h-1 w-full bg-gradient-to-r from-primary to-accent" />

        <div className="p-7 flex flex-col gap-5">

          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2 mb-1">
                <img src="/favicon.svg" alt="Orkly" className="w-9 h-9" />
                <span className="text-xs font-semibold text-primary uppercase tracking-widest">Orkly</span>
              </div>
              <h2 className="text-xl font-bold text-gray-900 leading-tight">
                {t('auth.welcome')}
              </h2>
              <p className="text-sm text-gray-600">
                {t('auth.subtitle')}
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition flex-shrink-0"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Google button */}
          <button
            onClick={signInWithGoogle}
            className="flex items-center justify-center gap-3 w-full border border-gray-200 rounded-xl px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-all hover:shadow-sm"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.875 2.684-6.615z" fill="#4285F4"/>
              <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z" fill="#34A853"/>
              <path d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05"/>
              <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z" fill="#EA4335"/>
            </svg>
            {t('auth.google')}
          </button>

          {/* Separador */}
          <div className="flex items-center gap-3">
            <div className="flex-1 h-px bg-gray-200" />
            <span className="text-xs text-gray-500">{t('auth.orEmail')}</span>
            <div className="flex-1 h-px bg-gray-200" />
          </div>

          {/* Magic link enviado */}
          {magicSent ? (
            <div className="text-center py-4 flex flex-col gap-2">
              <span className="text-3xl">📬</span>
              <p className="text-sm text-gray-700 font-medium">{t('auth.magicLinkSent')}</p>
            </div>
          ) : (
            <>
              {/* Email */}
              <div className="flex flex-col gap-3">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && !loading && handleEmailAuth()}
                  placeholder={t('auth.emailPlaceholder')}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 placeholder-gray-400 text-sm focus:outline-none focus:ring-2 focus:ring-primary transition"
                />

                {/* Password — solo en login y register */}
                {mode !== "magic" && (
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && !loading && handleEmailAuth()}
                    placeholder={t('auth.passwordPlaceholder')}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 placeholder-gray-400 text-sm focus:outline-none focus:ring-2 focus:ring-primary transition"
                  />
                )}
              </div>

              {/* Error */}
              {error && (
                <p className="text-xs text-red-500 bg-red-50 rounded-xl px-3 py-2">
                  {error}
                </p>
              )}

              {/* Botón principal */}
              {mode === "magic" ? (
                <button
                  onClick={handleMagicLink}
                  disabled={!email.trim() || loading}
                  className="w-full py-2.5 rounded-xl bg-primary text-white text-sm font-semibold hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition"
                >
                  {loading ? t('auth.sendingMagicLink') : t('auth.magicLink')}
                </button>
              ) : (
                <button
                  onClick={handleEmailAuth}
                  disabled={!email.trim() || !password.trim() || loading}
                  className="w-full py-2.5 rounded-xl bg-primary text-white text-sm font-semibold hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition"
                >
                  {loading
                    ? mode === "register" ? t('auth.registering') : t('auth.loggingIn')
                    : mode === "register" ? t('auth.register') : t('auth.login')
                  }
                </button>
              )}

              {/* Switch login/register/magic */}
              <div className="flex flex-col gap-1 text-center">
                {mode === "login" && (
                  <>
                    <p className="text-xs text-gray-500">
                      {t('auth.noAccount')}{" "}
                      <button onClick={() => { setMode("register"); setError(null); }} className="text-primary font-medium hover:underline">
                        {t('auth.switchToRegister')}
                      </button>
                    </p>
                    <button
                      onClick={() => { setMode("magic"); setError(null); }}
                      className="text-xs text-gray-400 hover:text-primary transition-colors"
                    >
                      {t('auth.magicLink')} →
                    </button>
                  </>
                )}
                {mode === "register" && (
                  <p className="text-xs text-gray-500">
                    {t('auth.hasAccount')}{" "}
                    <button onClick={() => { setMode("login"); setError(null); }} className="text-primary font-medium hover:underline">
                      {t('auth.switchToLogin')}
                    </button>
                  </p>
                )}
                {mode === "magic" && (
                  <button
                    onClick={() => { setMode("login"); setError(null); }}
                    className="text-xs text-gray-400 hover:text-primary transition-colors"
                  >
                    ← {t('auth.switchToLogin')}
                  </button>
                )}
              </div>
            </>
          )}

          {/* Footer note */}
          <p className="text-xs text-center text-gray-500 leading-relaxed">
            {t('auth.terms')}{" "}
            <a href="/terms" className="underline hover:text-gray-600 transition-colors">{t('auth.termsLink')}</a>
            {" "}{t('and')}{" "}
            <a href="/privacy" className="underline hover:text-gray-600 transition-colors">{t('auth.privacyLink')}</a>.
          </p>
        </div>
      </div>
    </div>
  );
}