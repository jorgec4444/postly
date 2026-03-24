import { useEffect, useState } from "react";
import { supabase } from "../supabase";
import { useNavigate, Outlet } from "react-router-dom";
import { toast } from 'react-hot-toast'

import Sidebar from "../components/Sidebar";

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
            <Sidebar />
             <main className="ml-64 p-8 min-h-screen bg-bg">
                <Outlet />
            </main>
        </div>
    );
}

export default Dashboard