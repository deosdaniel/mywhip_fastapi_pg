import React, {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import {login} from "../services/api";
import MyWhipLogo from "../components/MyWhipLogo.jsx";
import {Button} from "@/components/ui/button"
import {Input} from "@/components/ui/input.jsx"
import {Label} from "@/components/ui/label";
import {Loader2} from "lucide-react";

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
            newErrors.email = 'Введите email';
        } else if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
            newErrors.email = 'Некорректный формат email';
        }

        if (!formData.password) {
            newErrors.password = 'Введите пароль';
        } else if (formData.password.length < 8) {
            newErrors.password = 'Слишком короткий пароль';
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
        <div className='flex flex-col items-center
            justify-center h-screen p-8'>
            <div className="fixed top-8 left-1/2 transform -translate-x-1/2"><MyWhipLogo/></div>
            <div className='w-full max-w-md bg-white rounded-xl shadow-md p-6'>

                <h2 className='text-3xl font-bold mb-4 text-center'>Вход</h2>
                {serverError && (
                    <div className='mb-4 p-2 bg-red-100 text-red-700 rounded'>
                        {serverError}
                    </div>
                )}
                <form className='flex flex-col' onSubmit={handleSubmit}>
                    <div className=''>
                        <Label htmlFor="email"></Label>
                        <Input
                            id="email"
                            name="email"
                            type="email"
                            placeholder="your@mail.com"
                            className={errors.email ? "border-red-500" : ""}
                            value={formData.email}
                            onChange={handleChange}
                        />
                        <div className="min-h-5">
                            <p className={`text-red-500 text-sm transition-all duration-200 ${errors.email ? 'opacity-100' : 'opacity-0'}`}>
                                {errors.email}
                            </p>
                        </div>

                    </div>
                    <div className=''>
                        <Label htmlFor="password"></Label>
                        <Input
                            id="password"
                            name="password"
                            type="password"
                            placeholder="Пароль"
                            className={errors.password ? "border-red-500" : ""}
                            value={formData.password}
                            onChange={handleChange}
                        />
                        <div className="min-h-5">
                            <p className={`text-red-500 text-sm transition-all duration-200 
                            ${errors.password ? 'opacity-100' : 'opacity-0'}`}>
                                {errors.password}
                            </p>
                        </div>
                    </div>
                    <Button
                        className="mt-2"
                        variant="default"
                        type="submit"
                        disabled={isSubmitting}
                    >
                        {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin"/>}
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
    );
}

export default Login;