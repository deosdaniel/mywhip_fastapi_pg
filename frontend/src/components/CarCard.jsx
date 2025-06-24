import {Link} from "react-router-dom";
import carImg from "../assets/car_photo.jpg";

export default function CarCard({car}) {
    const image = car.image || carImg;
    return (
        <Link
            to={`/app/cars/${car.uid}`}
            className="flex flex-col bg-card hover:bg-accent rounded-md shadow-sm hover:shadow-md transition h-60 overflow-hidden"
        >
            <div className='h-full w-full overflow-hidden'>
                <div className="relative h-full flex">
                    <img src={image} alt={`${car.make} ${car.model}`}
                         className="w-full object-cover object-center"/>
                    <div
                        className="absolute inset-0 w-full bg-gradient-to-tr from-accent/20 to-transparent"></div>
                </div>
            </div>
            <div className="p-4 flex-1 flex-col justify-between">

                <h2 className="text-xl sm:text-xl font-semibold text-primary">{car.make} {car.model}</h2>
                <p className="text-gray-600 text-sm">{car.year}</p>
                <p className="text-sm text-blue-800">{car.status}</p>
            </div>
        </Link>
    );
}