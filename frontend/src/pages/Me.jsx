import {useEffect, useState} from 'react'
import api from '../services/api.js'
import {useNavigate} from "react-router-dom";

export default function Me() {
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/login';
    }
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await api.get('/auth/me');
                setUserData(response.data);
            } catch (err) {
                setError(err.response?.data?.detail || "Failed to fetch user data");
            } finally {
                setLoading(false);
            }
        };
        fetchUserData();
    }, []);

    if (loading) {
        return <div>Loading profile data...</div>
    }

    if (error) {
        return <div>Error: {error}</div>
    }


    return(
    <>
        <div className='flex flex-col items-center w-full max-w-md bg-[#222] rounded-xl
                 shadow-md py-8 px-8'>
            <h2 className='text-[28px] text-white font-bold mb-6
                     text-center'>Мой профиль</h2>
            {userData && (
                <div className='text-white'>
                    <p className='py-1'><strong>Email:</strong> {userData.email}</p>
                    <p className='py-1'><strong>Username:</strong> {userData.username}</p>
                    <p className='py-1'><strong>First name: </strong> {userData.first_name}</p>
                    <p className='py-1'><strong>Last name: </strong> {userData.last_name}</p>
                </div>
            )}
            <button className='mt-6 bg-gradient-to-r from-indigo-500
                                to-blue-500 text-white font-bold py-2 px-4 rounded-md
                                hover:bg-indigo-600 hover:to-blue-600 transition ease-in
                                duration-200 cursor-pointer'
                    onClick={() => navigate('/me/edit')}>
                Редактировать
            </button>
            <button className='mt-6 bg-gradient-to-r from-indigo-500
                                to-blue-500 text-white font-bold py-2 px-4 rounded-md
                                hover:bg-indigo-600 hover:to-blue-600 transition ease-in
                                duration-200 cursor-pointer'
                    onClick={handleLogout}>
                Выход
            </button>
        </div>
    </>
    );
}