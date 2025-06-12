import {Navigate, useNavigate} from 'react-router-dom';
import {useState, useEffect, } from "react";
import api from "../services/api";

export default function ProtectedRoute ({children}) {
    const [status, setStatus] = useState('checking');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setStatus('invalid');
      return;
    }

    api.get('/auth/validate', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(() => setStatus('valid'))
    .catch(() => {
      localStorage.removeItem('token');
      setStatus('invalid');
      navigate('/login');
    });
  }, [navigate]);

  if (status === 'checking') return <div>Loading...</div>;
  if (status === 'invalid') return <Navigate to="/login" replace />;
  return children;
}