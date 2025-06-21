import {Link, Outlet, useNavigate} from "react-router-dom";

export default function AppLayout() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div>
            <nav className="text-white">
                <Link to="cars">Мои автомобили</Link>
                <Link to="profile">Мой профиль</Link>
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