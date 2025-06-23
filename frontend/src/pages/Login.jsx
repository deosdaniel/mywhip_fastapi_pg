import React, {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import {login} from "../services/api";
import MyWhipLogo from "../components/MyWhipLogo.jsx";
import {Button} from "@/components/ui/button"
import {Input} from "@/components/ui/input.jsx"

function Login() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "",
        password: ""
    });
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [serverError, setServerError] = useState(null);

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
        // Очищаем ошибку при изменении поля
        if (errors[name]) {
            setErrors(prev => ({...prev, [name]: ""}));
        }
    };

    const validateForm = () => {
        const newErrors = {};

        if (!formData.email.trim()) {
            newErrors.email = 'Требуется email';
        } else if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
            newErrors.email = 'Некорректный формат email';
        }

        if (!formData.password) {
            newErrors.password = 'Требуется пароль';
        } else if (formData.password.length < 8) {
            newErrors.password = 'Пароль должен быть не короче 8 символов';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setServerError(null);

        if (!validateForm()) return;

        setIsSubmitting(true);

        try {
            const response = await login(formData.email, formData.password);
            console.log("Успешный вход: ", response);
            localStorage.setItem("token", response.access_token);
            navigate("/app");
        } catch (error) {
            console.error("Ошибка входа: ", error);
            setServerError(
                error.response?.data?.detail ||
                error.response?.data?.message ||
                "Ошибка при входе. Проверьте данные и попробуйте снова."
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div>

            <div className='flex flex-col items-center justify-center h-screen'>
                <MyWhipLogo/>
                <div className='w-full max-w-md bg-white rounded-xl shadow-md py-8 px-8'>

                    <h2 className='text-[28px] font-bold mb-2 text-center'>Вход</h2>

                    {/* Блок для отображения серверных ошибок */}
                    {serverError && (
                        <div className='mb-4 p-2 bg-red-100 text-red-700 rounded'>
                            {serverError}
                        </div>
                    )}

                    <form className='flex flex-col' onSubmit={handleSubmit}>
                        {/* Поле email с ошибкой */}
                        <div className='mb-4'>
                            <Input
                                name="email"
                                className=""
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="Email"
                            />
                            {errors.email && (
                                <p className="text-red-500 text-sm py-1">{errors.email}</p>
                            )}
                        </div>

                        {/* Поле пароля с ошибкой */}
                        <div className='mb-4'>
                            <Input
                                name="password"
                                className=""
                                type="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Пароль"
                            />
                            {errors.password && (
                                <p className="text-red-500 text-sm py-1">{errors.password}</p>
                            )}
                        </div>

                        {/* Кнопка с состоянием загрузки */}
                        <Button
                            className="btn"
                            type="submit"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Вход...' : 'Войти'}
                        </Button>

                        <p className='mt-4 text-center'>
                            Нет аккаунта?
                            <Link to='/signup' className='text-blue-400 hover:underline px-1'>
                                Зарегистрироваться
                            </Link>
                        </p>
                    </form>

                </div>
            </div>
        </div>
    );
}

export default Login;