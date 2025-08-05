import {NavLink, useNavigate} from "react-router-dom";
import {Button} from "@/components/ui/button.jsx";
import MyWhipLogo from "@/components/MyWhipLogo.jsx";
import {useState, useRef, useEffect} from "react";
import {Menu} from "lucide-react"

export default function NavBar() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const menuRef = useRef(null);
    const buttonRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (
                menuRef.current &&
                !menuRef.current.contains(event.target) &&
                buttonRef.current &&
                !buttonRef.current.contains(event.target)
            ) {
                setIsMenuOpen(false);
            }
        };

        document.addEventListener("click", handleClickOutside, true);
        return () => {
            document.removeEventListener("click", handleClickOutside, true);
        };
    }, []);

    const closeMenu = (cb) => () => {
        setIsMenuOpen(false);
        cb?.();
    };

    return (
        <div
            className="fixed top-0 left-0 right-0 z-50 flex justify-between items-center
      py-2 px-12 bg-white shadow
      md:px-36"
        >
            <MyWhipLogo className="scale-80 "></MyWhipLogo>

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
            <div
                ref={buttonRef}
                className={`md:hidden flex items-center cursor-pointer hover:bg-accent p-2 rounded-md ${isMenuOpen ? "bg-accent" : ""}`}>
                <Menu onClick={() => setIsMenuOpen(!isMenuOpen)}/>
            </div>
            <div
                ref={menuRef}
                className={`absolute md:hidden top-14 left-0 w-full bg-background flex flex-col items-center
    transition-all duration-300 ease-in-out
    ${isMenuOpen ? "opacity-100 translate-y-0 visible" : "opacity-0 translate-y-[-10px] invisible"}`}  // ← visible/invisible
            >
                <li className="list-none text-center">
                    <NavLink to="cars" onClick={closeMenu()}>
                        <Button variant="ghost">My Cars</Button>
                    </NavLink>
                </li>
                <li className="list-none text-center">
                    <NavLink to="profile" onClick={closeMenu()}>
                        <Button variant="ghost">My Profile</Button>
                    </NavLink>
                </li>
                <NavLink to="" onClick={closeMenu()}>
                    <Button variant="ghost">About</Button>
                </NavLink>
                <li className="list-none text-center">
                    <Button variant="ghost" onClick={closeMenu(logout)}>
                        Exit
                    </Button>
                </li>
            </div>
        </div>
    );
}
