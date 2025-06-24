import {Link} from "react-router-dom";
import carImg from "../assets/car_photo.jpg";
import {Button} from "@/components/ui/button.jsx";

export default function CarCard({car}) {
    const image = car.image || carImg;
    return (
        <Link
            to={`/app/cars/${car.uid}`}
            className="w-full flex flex-col bg-card hover:bg-accent rounded-md shadow-sm hover:shadow-md transition h-60 overflow-hidden"
        >
            <div className="h-full w-full flex overflow-hidden">
                <img src={image} alt={`${car.make} ${car.model}`}
                     className="w-full object-cover object-center"/>
            </div>
            <div className="flex px-4 p-2 items-center">
                <div className="flex flex-col justify-between w-full">
                    <h2 className="text-xl sm:text-xl font-semibold text-primary">{car.make} {car.model}</h2>
                    <p className="text-gray-600 text-sm">{car.year}</p>
                </div>
                <p className="text-primary bg-green-100 py-1 px-4 rounded-md border-white">{car.status}</p>

            </div>
        </Link>
    );
}