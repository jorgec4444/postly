import { supabase } from "../supabase";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function apiFetch(path, options = {}) {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;
  
  const isFormData = options.body instanceof FormData;
  
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const detail = err.detail;
    const message = typeof detail === 'string' 
      ? detail 
      : detail?.message || `HTTP ${res.status}`;
    throw new Error(message);
  }
  return res.status === 204 ? null : res.json();
}