import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://fmesbvfmwaumkauguxda.supabase.co'
const SUPABASE_ANON_KEY = 'tu-anon-key-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkdnNneWF0YXRlcWl6dGlzcmVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxNDIyNzgsImV4cCI6MjA3ODcxODI3OH0.k8C-VDMVi7pY39kW_-CXe9Dp0JrkcNOtkWpuf1xmN4k'

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)