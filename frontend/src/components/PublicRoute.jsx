import {Navigate} from 'react-router-dom';
import {useState, useEffect} from "react";
import api from "../services/api";

export default function PublicRoute({children}) {
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                setIsAuthenticated(false);
                return;
            }

            try {
                await api.get('/auth/validate', {
                    headers: {Authorization: `Bearer ${token}`}
                });
                setIsAuthenticated(true);
            } catch {
                setIsAuthenticated(false);
            }
        };

        checkAuth();
    }, []);

    if (isAuthenticated === null) return <div>Loading...</div>;
    if (isAuthenticated) return <Navigate to="/app/cars" replace/>;

    return children;
}