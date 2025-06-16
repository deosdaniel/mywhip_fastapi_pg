import {Navigate, useNavigate} from 'react-router-dom';
import {useState, useEffect, } from "react";
import api from "../services/api";

export default function ProtectedRoute({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        const validateToken = async () => {
            const token = localStorage.getItem('token');

            if (!token) {
                setIsAuthenticated(false);
                return;
            }

            try {
                // Простая проверка валидности токена
                await api.get('/auth/validate', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                setIsAuthenticated(true);
            } catch (error) {
                localStorage.removeItem('token');
                setIsAuthenticated(false);
            }
        };

        validateToken();
    }, []);

    if (isAuthenticated === null) {
        return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return children;
}