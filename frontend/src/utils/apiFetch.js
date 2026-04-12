import { supabase } from "../supabase";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function apiFetch(path, options = {}) {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;
  
  const isFormData = options.body instanceof FormData;
  const { raw = false, ...fetchOptions } = options;
  
  const res = await fetch(`${API_BASE}${path}`, {
    ...fetchOptions,
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...fetchOptions.headers,
    },
  });

  if (!res.ok && !raw) {
    const err = await res.json().catch(() => ({}));
    const detail = err.detail;
    const message = typeof detail === 'string' 
      ? detail 
      : detail?.message || `HTTP ${res.status}`;
    throw new Error(message);
  }

  if (raw) return res;
  return res.status === 204 ? null : res.json();
}