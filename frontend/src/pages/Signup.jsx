import React, {useState} from 'react'
import {Link, useNavigate} from "react-router-dom";
import api from '../services/api.js'
import MyWhipLogo from "../components/MyWhipLogo.jsx";

const Signup = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        confirmPassword: '',
    });
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [serverError, setServerError] = useState(null);

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
        if (errors[name]) {
            setErrors(prev => ({...prev, [name]: errors[name]}));
        }
    }
    const validateForm = () => {
        const newErrors = {};

        if (!formData.username.trim()) newErrors.username = 'Требуется имя пользователя';
        if (!formData.email.trim()) newErrors.email = 'Требуется email';
        else if (!/^\S+@\S+\.\S+$/.test(formData.email)) newErrors.email = 'Некорректный email';
        if (!formData.first_name.trim()) newErrors.first_name = 'Требуется имя';
        if (!formData.last_name.trim()) newErrors.last_name = 'Требуется фамилия';
        if (!formData.password) newErrors.password = 'Требуется пароль';
        else if (formData.password.length < 8) newErrors.password = 'Пароль должен быть не короче 8 символов';
        if (formData.password !== formData.confirmPassword) newErrors.confirmPassword = 'Пароли не совпадают';

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setServerError(null);
        if (!validateForm()) return;

        setIsSubmitting(true);

        try {
            const payload = {
                username: formData.username,
                email: formData.email,
                first_name: formData.first_name,
                last_name: formData.last_name,
                password: formData.password
            };
            const response = await api.post('/users/signup', payload);
            console.log('User created successfully', response.data);
            alert("Поздравляем, вы успешно зарегистрированы!")
            navigate('/login');
        } catch (error) {
            setServerError(
                error.response?.data?.detail ||
                error.response?.data?.message ||
                'Error occurred while creating new user'
            );
        } finally {
            setIsSubmitting(false);

        }
    };


    return (
        <div>
            <div className='flex flex-col items-center
            justify-center h-screen '>
                <MyWhipLogo/>
                <div className='w-full max-w-md bg-[#222] rounded-xl
                 shadow-md py-8 px-8'>
                    <h2 className='text-[28px] text-white font-bold mb-6
                     text-center'>Регистрация</h2>
                    {serverError && (
                        <div className='mb-4 p-2 bg-red-100 text-red-700 rounded'>
                            {serverError}
                        </div>
                    )}
                    <form onSubmit={handleSubmit} className='flex flex-col'>
                        <div className='flex space-x-4 mb-4'>
                            <div className='w-1/2'>
                                <input
                                    name='first_name'
                                    placeholder='Имя'
                                    className={`bg-gray-600 text-white border-0 rounded-md p-2 w-full
                                    focus:bg-gray-400 focus:outline-none transition ease-in-out duration-150
                                    placeholder-gray-300 ${errors.first_name ? 'border-red-500' : ''}`}
                                    type='text'
                                    value={formData.first_name}
                                    onChange={handleChange}
                                />
                                {errors.first_name && <p className='text-red-500 text-sm mt-1'>{errors.first_name}</p>}
                            </div>
                            <div className='w-1/2'>
                                <input
                                    name='last_name'
                                    placeholder='Фамилия'
                                    className={`bg-gray-600 text-white border-0 rounded-md p-2 w-full
                                    focus:bg-gray-400 focus:outline-none transition ease-in-out duration-150
                                    placeholder-gray-300 ${errors.last_name ? 'border-red-500' : ''}`}
                                    type='text'
                                    value={formData.last_name}
                                    onChange={handleChange}
                                />
                                {errors.last_name && <p className='text-red-500 text-sm mt-1'>{errors.last_name}</p>}
                            </div>
                        </div>
                        <div className='mb-4'>
                            <input
                                name='username'
                                placeholder='Имя пользователя'
                                className={`bg-gray-600 text-white border-0 rounded-md p-2 w-full
                                focus:bg-gray-400 focus:outline-none transition ease-in-out duration-150
                                placeholder-gray-300 ${errors.username ? 'border-red-500' : ''}`}
                                type='text'
                                value={formData.username}
                                onChange={handleChange}
                            />
                            {errors.username && <p className='text-red-500 text-sm mt-1'>{errors.username}</p>}
                        </div>

                        <div className='mb-4'>
                            <input
                                name='email'
                                placeholder='Эл. почта'
                                className={`bg-gray-600 text-white border-0 rounded-md p-2 w-full
                                focus:bg-gray-400 focus:outline-none transition ease-in-out duration-150
                                placeholder-gray-300 ${errors.email ? 'border-red-500' : ''}`}
                                type='email'
                                value={formData.email}
                                onChange={handleChange}
                            />
                            {errors.email && <p className='text-red-500 text-sm mt-1'>{errors.email}</p>}
                        </div>

                        <div className='mb-4'>
                            <input
                                name='password'
                                placeholder='Пароль'
                                className={`bg-gray-600 text-white border-0 rounded-md p-2 w-full
                                focus:bg-gray-400 focus:outline-none transition ease-in-out duration-150
                                placeholder-gray-300 ${errors.password ? 'border-red-500' : ''}`}
                                type='password'
                                value={formData.password}
                                onChange={handleChange}
                            />
                            {errors.password && <p className='text-red-500 text-sm mt-1'>{errors.password}</p>}
                        </div>
                        <div className='mb-4'>
                            <input
                                name='confirmPassword'
                                placeholder='Подтвердите пароль'
                                className={`bg-gray-600 text-white border-0 rounded-md p-2 w-full
                                focus:bg-gray-400 focus:outline-none transition ease-in-out duration-150
                                placeholder-gray-300 ${errors.confirmPassword ? 'border-red-500' : ''}`}
                                type='password'
                                value={formData.confirmPassword}
                                onChange={handleChange}
                            />
                            {errors.confirmPassword &&
                                <p className='text-red-500 text-sm mt-1'>{errors.confirmPassword}</p>}
                        </div>
                        <button
                            className='bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-bold py-2 px-4 rounded-md
                            hover:bg-indigo-600 hover:to-blue-600 transition ease-in duration-200 cursor-pointer
                            disabled:opacity-50'
                            type='submit'
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Регистрация...' : 'Зарегистрироваться'}
                        </button>
                        <p className='text-white mt-4 text-center'>
                            Уже есть аккаунт?
                            <Link to='/login' className='text-blue-400 hover:underline mt-4 px-1'>
                                Войти
                            </Link>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Signup