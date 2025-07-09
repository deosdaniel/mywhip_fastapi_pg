import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

export default function MyWhipLogo({ className }) {
  return (
    <Link to="/">
      <div className={`flex items-center justify-center gap-x-4 ${className}`}>
        <img
          src={logo}
          alt="my_whip_logo"
          className="h-10 w-auto object-contain"
        />
        <div className="flex flex-row gap-x-2">
          <p className="text-text font-bold text-2xl">My</p>
          <p className="text-text font-bold text-2xl">Whip</p>
        </div>
      </div>
    </Link>
  );
}
