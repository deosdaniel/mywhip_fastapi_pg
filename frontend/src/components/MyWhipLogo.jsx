import {Link} from "react-router-dom";
import logo from "../assets/logo.png"


export default function MyWhipLogo() {
    return (
        <Link to="/">
            <div className='flex items-center justify-center gap-x-8 py-2'>
                <img src={logo} alt="my_whip_logo" className="h-20 w-auto object-contain"/>
                <div className="flex flex-col">
                    <p className="text-text font-bold text-3xl">My</p>
                    <p className="text-text font-bold text-3xl">Whip</p>
                </div>
            </div>
        </Link>
    )
}