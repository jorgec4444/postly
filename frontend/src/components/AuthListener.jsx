import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabase'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'

function AuthListener() {
    const navigate = useNavigate();
    const { t } = useTranslation();

    useEffect(() => {
        const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
            if (event === 'SIGNED_IN' && session) {
                if (window.location.pathname === '/' || window.location.hash.includes('access_token')) {
                    toast.success(t('auth.welcomeToast'), {
                        duration: 4000,
                        icon: '🎉',
                    });
                    navigate('/dashboard');
                }
            }
        });

        return () => subscription.unsubscribe();
    }, [])

    return null
}

export default AuthListener