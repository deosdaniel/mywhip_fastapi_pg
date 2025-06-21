import {Link, NavLink, Outlet, useNavigate} from "react-router-dom";
import MyWhipLogo from "../components/MyWhipLogo.jsx";
import logo from "../assets/logo.png";

export default function AppLayout() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div>
            <nav className="flex justify-center items-center bg-blue-800 text-white gap-2">
                <Link to="/">
                    <div className='flex items-center justify-center gap-x-2 '>
                        <img src={logo} alt="my_whip_logo" className="h-10 w-auto object-contain"/>
                        <div className="flex flex-col">
                            <p className="text-white font-bold">My</p>
                            <p className="text-white font-bold">Whip</p>
                        </div>
                    </div>
                </Link>
                <div>
                    <NavLink to="cars" className={({isActive}) => isActive ? "text-blue-300" : ""}>
                        Мои автомобили</NavLink>
                </div>
                <div>
                    <NavLink to="profile" className={({isActive}) => isActive ? "text-blue-300" : ""}>Мой
                        профиль</NavLink>
                </div>
                <button onClick={logout}>
                    <p className="cursor-pointer">Выйти</p>
                </button>
            </nav>
            <main>
                <Outlet/>
            </main>
        </div>
    );
};