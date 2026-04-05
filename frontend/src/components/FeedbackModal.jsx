import { useState } from "react";
import { toast } from "react-hot-toast";
import { useTranslation } from "react-i18next";
import { supabase } from "../supabase";
import Button from "./Button";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function FeedbackModal({ onClose }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const { t } = useTranslation();

  

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const headers = { "Content-Type": "application/json" };
      if (session?.access_token) {
        headers["Authorization"] = `Bearer ${session.access_token}`;
      }

      await fetch(`${API_BASE}/feedback/save`, {
        method: "POST",
        headers,
        body: JSON.stringify({ feedback: text.trim() }),
      });
      setSent(true);
      setTimeout(onClose, 1500);
    } catch (e) {
      toast.error(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

    return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-white border border-gray-200 rounded-2xl shadow-2xl w-full max-w-sm mx-4 overflow-hidden">
        <div className="h-1 w-full bg-gradient-to-r from-primary to-accent" />
        <div className="p-6 flex flex-col gap-4">
          <div>
            <h2 className="text-base font-bold text-gray-900">{t('feedback.title')}</h2>
            <p className="text-sm text-gray-600 mt-0.5">{t('feedback.subtitle')}</p>
          </div>
          {sent ? (
            <p className="text-sm text-primary font-medium py-4 text-center">{t('feedback.thanks')}</p>
          ) : (
            <>
              <textarea
                autoFocus
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder={t('feedback.placeholder')}
                rows={4}
                className="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 placeholder-gray-400 text-sm focus:outline-none focus:ring-2 focus:ring-primary transition resize-none"
              />
              <div className="flex gap-2 justify-end">
                <Button variant="secondary" onClick={onClose}>
                  {t('feedback.cancel')}
                </Button>
                <Button onClick={handleSubmit} disabled={!text.trim()} loading={loading}>
                  {t('feedback.send')}
                </Button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

