import {Link} from "react-router-dom";
import logo from "../assets/logo.png"

export default function MyWhipLogo() {
    return (
        <Link to="/">
            <div className='flex items-center justify-center gap-x-6'>
                <img src={logo} alt="my_whip_logo" className="h-20 object-cover"/>
                <p className="text-white font-bold text-3xl">My Whip</p>
            </div>
        </Link>
    )
}