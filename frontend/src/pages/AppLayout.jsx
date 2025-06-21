import {Link, NavLink, Outlet, useNavigate} from "react-router-dom";

export default function AppLayout() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div>
            <nav className="flex justify-center text-white gap-2">
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