import {Link} from "react-router-dom";
import carImg from "../assets/car_photo.jpg";

export default function CarCard({car}) {
    const image = car.image || carImg;
    return (
        <Link
            to={`/app/cars/${car.uid}`}
            className="flex flex-col bg-gray-200 hover:bg-gray-300 rounded-xl shadow hover:shadow-md transition h-60 overflow-hidden"
        >
            <div className='h-40 w-full overflow-hidden'>
                <img src={image} alt={`${car.make} ${car.model}`} className="w-full h-full object-cover "/>
            </div>
            <div className="p-4 flex-1 flex-col justify-between">

                <h2 className="text-xl sm:text-xl font-semibold">{car.make} {car.model}</h2>
                <p className="text-gray-600 text-sm">{car.year}</p>
                <p className="text-sm text-blue-800 ">{car.status}</p>
            </div>
        </Link>
    );
}