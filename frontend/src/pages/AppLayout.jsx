import {Link, NavLink, Outlet, useNavigate} from "react-router-dom";
import logo from "../assets/logo.png";

import NavBar from "../components/NavBar.jsx";

export default function AppLayout() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div className="min-h-screen">
            <NavBar/>
            <main className="pt-16">
                <Outlet/>
            </main>
        </div>
    );
}
