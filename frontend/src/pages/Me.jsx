import {useEffect, useState} from 'react'
import api from '../services/api.js'
import {useNavigate} from "react-router-dom";
import EditIcon from "../components/EditIcon.jsx";

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
        return <div>Загрузка профиля...</div>
    }

    if (error) {
        return <div>Ошибка: {error}</div>
    }


    return(
    <>
        <div className='flex flex-col items-center w-full max-w-md bg-[#222] rounded-xl
                 shadow-md py-8 px-8'>
            <div className='flex items-center justify-between gap-2 mb-6'>
                <h2 className='text-[28px] text-white font-bold
                         text-center'>Мой профиль</h2>
                <button className='bg-gradient-to-r from-indigo-500
                                    to-blue-500 text-white font-bold py-1 px-1 rounded-md
                                    hover:bg-indigo-600 hover:to-blue-600 transition ease-in
                                    duration-200 cursor-pointer'
                        onClick={() => navigate('/me/edit')}>
                    <EditIcon/>
                </button>
            </div>
            {userData && (
                <div className='text-white'>
                    <p className='py-1'>Эл. почта: <strong>{userData.email}</strong> </p>
                    <p className='py-1'>Никнейм: <strong>{userData.username}</strong> </p>
                    <p className='py-1'>Имя: <strong>{userData.first_name}</strong> </p>
                    <p className='py-1'>Фамилия: <strong>{userData.last_name}</strong></p>
                </div>
            )}

            <button className='mt-6 bg-gradient-to-r from-indigo-500
                                to-blue-500 text-white font-bold py-2 px-4 rounded-md
                                hover:from-indigo-500 hover:to-blue-600 transition ease-in
                                duration-200 cursor-pointer'
                    onClick={handleLogout}>
                Выйти
            </button>
        </div>
    </>
    );
}