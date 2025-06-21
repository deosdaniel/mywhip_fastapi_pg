import {Link} from "react-router-dom";
import React from "react";

function Home() {
    return (
        <div>
            <Link to='/signup' className='text-white hover:underline px-1'>
                Зарегистрироваться
            </Link>
        </div>
    )
}

export default Home;

