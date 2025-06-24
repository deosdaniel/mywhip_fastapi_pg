import {NavLink, useNavigate} from "react-router-dom";
import {Button} from "@/components/ui/button.jsx";
import MyWhipLogo from "@/components/MyWhipLogo.jsx";
import {useState} from "react";

export default function NavBar() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <div
            className="fixed top-0 left-0 right-0 flex justify-between items-center
      py-2 px-12 bg-white shadow
      md:px-36"
        >
            <a>
                <MyWhipLogo className="scale-80 "></MyWhipLogo>
            </a>
            <ul className="hidden md:flex items-center gap-2">
                <li>
                    <NavLink to="cars">
                        <Button variant="ghost">My Cars</Button>
                    </NavLink>
                </li>
                <li>
                    <NavLink to="profile">
                        <Button variant="ghost">My Profile</Button>
                    </NavLink>
                </li>
                <li>
                    <NavLink to="">
                        <Button variant="ghost">About</Button>
                    </NavLink>
                </li>
            </ul>
            <div className="relative hidden md:flex">
                <Button variant="ghost" onClick={logout}>
                    Exit
                </Button>
            </div>
            <div className="md:hidden flex items-center">
                <i
                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                    className=" bx bx-menu cursor-pointer  text-3xl block  "
                ></i>
            </div>
            <div
                className={`absolute md:hidden top-14 left-0 w-full bg-background flex flex-col items-center
    transition-all duration-300 ease-in-out
    ${isMenuOpen ? "opacity-100 translate-y-0 visible" : "opacity-0 translate-y-[-10px] invisible"}`}  // ← visible/invisible
            >
                <li className="list-none text-center">
                    <NavLink to="cars">
                        <Button variant="ghost">My Cars</Button>
                    </NavLink>
                </li>
                <li className="list-none text-center">
                    <NavLink to="profile">
                        <Button variant="ghost">My Profile</Button>
                    </NavLink>
                </li>
                <NavLink to="">
                    <Button variant="ghost">About</Button>
                </NavLink>
                <li className="list-none text-center">
                    <Button variant="ghost" onClick={logout}>
                        Exit
                    </Button>
                </li>
            </div>
        </div>
    );
}
