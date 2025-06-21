import {Link, NavLink, Outlet, useNavigate} from "react-router-dom";

export default function AppLayout() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div>
            <nav className="text-white">
                <NavLink to="cars" className={({isActive}) => isActive ? "text-blue-300" : ""}>Мои автомобили</NavLink>
                <NavLink to="profile" className={({isActive}) => isActive ? "text-blue-300" : ""}>Мой профиль</NavLink>
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