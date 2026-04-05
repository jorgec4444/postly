import { useState } from "react";
import { useTranslation } from "react-i18next";
import { toast } from "react-hot-toast";
import FeedbackModal from "./FeedbackModal";

export default function Footer() {
  const [showFeedback, setShowFeedback] = useState(false);
  const { t } = useTranslation();

  return (
    <>
      <footer className="mt-16 border-t border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-6">

          {/* Left — brand */}
          <div className="flex items-center gap-2.5">
            <img src="/favicon.svg" alt="Orkly" className="w-6 h-6 opacity-70" />
            <span className="text-xs text-gray-400 tracking-wide">
              © {new Date().getFullYear()} Orkly
            </span>
          </div>

          {/* Center / Right — links */}
          <div className="flex items-center gap-6 flex-wrap justify-center">
            <button
              onClick={() => setShowFeedback(true)}
              className="text-xs text-gray-400 hover:text-primary transition-colors"
            >
              {t('footer.feedback')}
            </button>
            <a href="/pricing" className="text-xs text-gray-400 hover:text-primary transition-colors">
              {t('footer.pricing')}
            </a>
            <a href="/terms" className="text-xs text-gray-400 hover:text-primary transition-colors">
              {t('footer.terms')}
            </a>
            <a href="/privacy" className="text-xs text-gray-400 hover:text-primary transition-colors">
              {t('footer.privacy')}
            </a>
            <a
              href="mailto:jorgecdev444@gmail.com"
              className="text-xs text-gray-400 hover:text-primary transition-colors"
            >
              {t('footer.contact')}
            </a>
            <a
              href="https://x.com/jorgecdev444"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-gray-400 hover:text-primary transition-colors"
            >
              𝕏
            </a>
          </div>
        </div>
      </footer>

      {showFeedback && <FeedbackModal onClose={() => setShowFeedback(false)} />}
    </>
  );
}