import {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import api from '../services/api.js';

export default function EditProfile() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
    });
    const [userUid, setUserUid] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [successfulMessage, setSuccessfulMessage] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await api.get('/auth/me');
                setFormData({
                    username: response.data.username || '',
                    first_name: response.data.first_name || '',
                    last_name: response.data.last_name || ''
                });
                if (!response.data.uid || typeof response.data.uid !== 'string') {
                    throw new Error('Invalid username UID format');
                }
                setUserUid(response.data.uid);

                setError(null);
            } catch (error) {
                console.error('Failed to fetch user data: ', error);
                setError(error.response?.data?.detail || "Не удалось получить данные о пользователе :(");
            } finally {
                setLoading(false);
            }
        };
        fetchUserData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();


        if (!formData.username.trim()) {
            setError('Username обязателен');
            return;
        }

        setIsSubmitting(true);
        setError(null);
        setSuccessfulMessage(null);

        try {
            const response = await api.patch(`/users/${userUid}`, formData);
            console.log('Update successful:', response.data);

            // Перенаправляем с небольшим таймаутом для UX
            setTimeout(() => navigate('/me'), 1000);
        } catch (err) {
            console.error('Update failed:', err);
            // Подробный анализ ошибки
            const errorMessage = err.response?.data?.detail
                || err.response?.data?.message
                || err.message
                || 'Не удалось обновить данные профиля';
            setError(errorMessage);

            // Особый случай 403
            if (err.response?.status === 403) {
                setError('Нет доступа. Возможно, требуется войти заново.');
            }
        } finally {
            setIsSubmitting(false);
        }
    };
    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="text-white">Загрузка данных профиля...</div>
            </div>
        );
    }

    if (error && !loading) {
        return (
            <div className="flex flex-col items-center">
                <div className="text-red-500 mb-8">{error}</div>
                <button onClick={() => window.location.reload()} className="bg-blue-500 text-white px-4 py-2 rounded">
                    Попробовать снова
                </button>
            </div>
        );
    }
    return (
        <div className='flex flex-col items-center w-full max-w-md bg-[#222] rounded-xl shadow-md py-8 px-8 mx-auto mt-10'>
            <h2 className='text-[28px] text-white font-bold mb-6 text-center'>
                Изменить данные профиля
            </h2>
            {successfulMessage && (
                <div className="mb-4 p-2 bg-green-100 text-green-800 rounded">
                    {successfulMessage}
                </div>
            )}
            <form onSubmit={handleSubmit} className='w-full'>
                <div className='mb-4'>
                    <label className='block text-white mb-2'> Username *</label>
                    <input
                        type="text"
                        name='username'
                        value={formData.username}
                        onChange={handleChange}
                        className='w-full bg-gray-600 text-white border-0 rounded-md p-2 focus:bg-gray-400 focus:outline-none transition duration-150'
                        required
                    />
                </div>
                <div>
                    <label className='block text-white mb-2'>Имя</label>
                    <input
                        type='text'
                        name='first_name'
                        value={formData.first_name}
                        onChange={handleChange}
                        className='w-full bg-gray-600 text-white border-0 rounded-md p-2 focus:bg-gray-400 focus:outline-none transition duration-150'
                    />
                </div>
                <div>
                    <label className='block text-white mb-2'>Фамилия</label>
                    <input
                        type='text'
                        name='last_name'
                        value={formData.last_name}
                        onChange={handleChange}
                        className='w-full bg-gray-600 text-white border-0 rounded-md p-2 focus:bg-gray-400 focus:outline-none transition duration-150'
                    />
                </div>
                <div className='flex justify-between'>
                    <button
                        type='button'
                        onClick={() => navigate('/me')}
                        className='bg-gray-500 text-white font-bold py-2 px-4 rounded-md hover:bg-gray-600 transition duration-200'
                        disabled={isSubmitting}
                    >
                        Отмена
                    </button>
                    <button
                        type='submit'
                        className='bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-indigo-600 transition duration-200'
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? 'Сохранение...' : 'Сохранить'}
                    </button>
                </div>
            </form>
        </div>
    );
}