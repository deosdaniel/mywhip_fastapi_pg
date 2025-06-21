import {Link} from "react-router-dom";
import carImg from "../assets/car_poster.jpg";

export default function CarCard({car}) {
    const image = car.image || carImg;
    return (
        <Link
            to={`/app/cars/${car.uid}`}
            className="flex flex-col bg-amber-100 rounded-xl shadow hover:shadow-md transition h-60 overflow-hidden"
        >
            <div className='h-40 w-full overflow-hidden'>
                <img src={image} alt={`${car.make} ${car.model}`} className="w-full h-full object-cover "/>
            </div>
            <div className="p-4 flex-1 flex-col justify-between">

                <h2 className="text-xl font-semibold">{car.make} {car.model}</h2>
                <p className="text-gray-600">Год: {car.year}</p>
                <p className="text-sm text-blue-600">Статус: {car.status}</p>
            </div>
        </Link>
    );
}