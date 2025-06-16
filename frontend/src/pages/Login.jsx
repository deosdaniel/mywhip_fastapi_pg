import React, { useState } from "react";
import {Link, useNavigate} from "react-router-dom";
import {login} from "../services/api";


function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await login(email,password)
            console.log("Успешный ответ: ", response)
            localStorage.setItem("token", response.access_token);
            navigate("/dashboard")
        } catch (error) {
            console.log("Ошибка входа: ",error.response?.data || error);
        }
    }
    return (
        <div>
            <div className='flex flex-col items-center
            justify-center h-screen '>
                <div className='w-full max-w-md bg-[#222] rounded-xl
                 shadow-md py-8 px-8'>
                    <h2 className='text-[28px] text-white font-bold mb-6
                     text-center'>Вход</h2>
                    <form className='flex flex-col' onSubmit={handleSubmit}>

                        <input className='bg-gray-600
                                    text-white  border-0 rounded-md p-2 mb-4
                                    focus:bg-gray-400 focus:outline-none
                                    transition ease-in-out duration-150
                                    placeholder-gray-300'
                               type="email"
                               value={email}
                               onChange={(e) => setEmail(e.target.value)}
                               placeholder="Email"
                        />
                        <input className='bg-gray-600
                                    text-white  border-0 rounded-md p-2 mb-4
                                    focus:bg-gray-400 focus:outline-none
                                    transition ease-in-out duration-150
                                    placeholder-gray-300'
                               type="password"
                               value={password}
                               onChange={(e) => setPassword(e.target.value)}
                               placeholder="Password"
                        />
                        <button className='bg-gradient-to-r from-indigo-500
                                to-blue-500 text-white font-bold py-2 px-4 rounded-md
                                hover:bg-indigo-600 hover:to-blue-600 transition ease-in
                                duration-200 cursor-pointer' type='submit'>Войти
                        </button>
                        <p className='text-white mt-4 text-center'>Нет аккаунта?
                            <Link to='/signup' className='text-white-500 hover:underline mt-4 px-1'>
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