import { useEffect, useState } from "react";
import { supabase } from "../supabase";
import { useNavigate } from "react-router-dom";
import { toast } from 'react-hot-toast'

function Dashboard() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function checkSession() {
            const { data: { session } } = await supabase.auth.getSession();
            if (!session) {
                toast.error('You need to be logged in to access the dashboard')
                navigate("/");
            }
            setLoading(false);
        }
        checkSession();
    }, []);

    if (loading) return;

    return (
        <div>
            <h1>Welcome to the Dashboard</h1>
        </div>
    );
}

export default Dashboard