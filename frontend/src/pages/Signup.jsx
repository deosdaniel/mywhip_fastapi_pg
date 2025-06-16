import React from 'react'
import {Link} from "react-router-dom";

const Signup = () => {

    return (
        <div>
            <div className='flex flex-col items-center
            justify-center h-screen '>
                <div className='w-full max-w-md bg-[#222] rounded-xl
                 shadow-md py-8 px-8'>
                    <h2 className='text-[28px] text-white font-bold mb-6
                     text-center'>Регистрация</h2>
                    <form className='flex flex-col'>
                        <div className='flex space-x-4 mb-4'>
                            <input placeholder='Имя' className='bg-gray-600
                            text-white  border-0 rounded-md p-2 w-1/2
                            focus:bg-gray-400 focus:outline-none
                            transition ease-in-out duration-150
                            placeholder-gray-300' type='text'/>
                            <input placeholder='Фамилия' className='bg-gray-600
                            text-white  border-0 rounded-md p-2 w-1/2
                            focus:bg-gray-400 focus:outline-none
                            transition ease-in-out duration-150
                            placeholder-gray-300' type='text'/>
                        </div>
                        <input placeholder='Эл. почта' className='bg-gray-600
                            text-white  border-0 rounded-md p-2 mb-4
                            focus:bg-gray-400 focus:outline-none
                            transition ease-in-out duration-150
                            placeholder-gray-300' type='email'/>
                        <input placeholder='Пароль' className='bg-gray-600
                            text-white  border-0 rounded-md p-2 mb-4
                            focus:bg-gray-400 focus:outline-none
                            transition ease-in-out duration-150
                            placeholder-gray-300' type='password'/>
                        <input placeholder='Подтвердите пароль' className='bg-gray-600
                            text-white  border-0 rounded-md p-2 mb-4
                            focus:bg-gray-400 focus:outline-none
                            transition ease-in-out duration-150
                            placeholder-gray-300' type='password'/>
                        <button className='bg-gradient-to-r from-indigo-500
                        to-blue-500 text-white font-bold py-2 px-4 rounded-md
                        hover:bg-indigo-600 hover:to-blue-600 transition ease-in
                        duration-200 cursor-pointer' type='submit'>
                            Зарегистрироваться
                        </button>
                        <p className='text-white mt-4 text-center'>
                            Уже есть аккаунт?
                            <Link to='/login' className='text-white-500 hover:underline mt-4 px-1'>
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