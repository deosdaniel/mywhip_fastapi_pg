import {Link, NavLink, Outlet, useNavigate} from "react-router-dom";
import logo from "../assets/logo.png";

export default function AppLayout() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div className="min-h-screen ">
            <nav className="flex  flex-wrap items-center justify-between px-4 py-2 bg-[#222] text-white mb-4">
                <Link to="/" className="flex items-center gap-2">
                    <img src={logo} alt="my_whip_logo" className="h-10 w-auto object-contain"/>
                    <div className="flex flex-col leading-none">
                        <span className="font-bold">My</span>
                        <span className="font-bold">Whip</span>
                    </div>
                </Link>

                <div className="flex sm:flex-row sm:items-center gap-4 px-4">
                    <NavLink to="cars" className={({isActive}) => isActive ? "text-blue-300" : ""}>
                        Мои автомобили
                    </NavLink>
                    <NavLink to="profile" className={({isActive}) => isActive ? "text-blue-300" : ""}>
                        Мой профиль
                    </NavLink>
                    <button onClick={logout} className="text-white hover:text-red-300 transition">
                        Выйти
                    </button>
                </div>
            </nav>
            <main>
                <Outlet/>
            </main>
        </div>
    );
};