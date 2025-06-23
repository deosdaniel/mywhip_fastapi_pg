import React, {useState} from 'react'
import {Link, useNavigate} from "react-router-dom";
import api from '../services/api.js'
import MyWhipLogo from "../components/MyWhipLogo.jsx";
import {Button} from "@/components/ui/button"
import {Input} from "@/components/ui/input.jsx"
import {Label} from "@/components/ui/label";
import {Loader2} from "lucide-react";

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
        <div className='flex flex-col items-center
            justify-center h-screen p-8'>
            <div className="fixed top-8 left-1/2 transform -translate-x-1/2"><MyWhipLogo/></div>
            <div className='w-full max-w-md bg-white rounded-xl shadow-md p-6'>
                <h2 className='text-3xl font-bold mb-4 text-center'>Регистрация</h2>
                {serverError && (
                    <div className='mb-4 p-2 bg-red-100 text-red-700 rounded'>
                        {serverError}
                    </div>
                )}
                <form className='flex flex-col' onSubmit={handleSubmit}>
                    <div className='flex space-x-4 mb-4'>
                        <div className='w-1/2'>
                            <Input
                                name='first_name'
                                placeholder='Имя'
                                className={errors.first_name ? "border-red-500" : ""}
                                type='text'
                                value={formData.first_name}
                                onChange={handleChange}
                            />
                            {errors.first_name && <p className='text-red-500 text-sm mt-1'>{errors.first_name}</p>}
                        </div>
                        <div className='w-1/2'>
                            <Input
                                name='last_name'
                                placeholder='Фамилия'
                                className={errors.last_name ? 'border-red-500' : ''}
                                type='text'
                                value={formData.last_name}
                                onChange={handleChange}
                            />
                            {errors.last_name && <p className='text-red-500 text-sm mt-1'>{errors.last_name}</p>}
                        </div>
                    </div>
                    <div className='mb-4'>
                        <Label htmlFor="username"></Label>
                        <Input
                            name='username'
                            placeholder='Имя пользователя*'
                            className={errors.username ? 'border-red-500' : ''}
                            type='text'
                            value={formData.username}
                            onChange={handleChange}
                        />
                        {errors.username && <p className='text-red-500 text-sm mt-1'>{errors.username}</p>}
                    </div>

                    <div className='mb-4'>
                        <Label htmlFor="email"></Label>
                        <Input
                            name='email'
                            placeholder='Эл. почта*'
                            className={errors.email ? 'border-red-500' : ''}
                            type='email'
                            value={formData.email}
                            onChange={handleChange}
                        />
                        {errors.email && <p className='text-red-500 text-sm mt-1'>{errors.email}</p>}
                    </div>

                    <div className='mb-4'>
                        <Label htmlFor="password"></Label>
                        <Input
                            name='password'
                            placeholder='Пароль*'
                            className={errors.password ? 'border-red-500' : ''}
                            type='password'
                            value={formData.password}
                            onChange={handleChange}
                        />
                        {errors.password && <p className='text-red-500 text-sm mt-1'>{errors.password}</p>}
                    </div>
                    <div className='mb-4'>
                        <Label htmlFor="confirmPassword"></Label>
                        <Input
                            name='confirmPassword'
                            placeholder='Подтвердите пароль*'
                            className={errors.confirmPassword ? 'border-red-500' : ''}
                            type='password'
                            value={formData.confirmPassword}
                            onChange={handleChange}
                        />
                        {errors.confirmPassword &&
                            <p className='text-red-500 text-sm mt-1'>{errors.confirmPassword}</p>}
                    </div>
                    <Button
                        variant="default"
                        type="submit"
                        disabled={isSubmitting}
                    >
                        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin"/>}
                        {isSubmitting ? 'Регистрация...' : 'Зарегистрироваться'}
                    </Button>
                    <p className='mt-4 text-center'>
                        Уже есть аккаунт?
                        <Link to='/login' className='text-blue-400 hover:underline mt-4 px-1'>
                            Войти
                        </Link>
                    </p>
                </form>
            </div>
        </div>
    )
}

export default Signup