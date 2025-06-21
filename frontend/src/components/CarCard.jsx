import {Link} from "react-router-dom";

export default function CarCard({car}) {
    return (
        <Link
            to={`/app/cars/${car.id}`}
            className="block bg-white rounded-xl shadow hover:shadow-md transition overflow-hidden"
        >
            <img src={car.image} alt={`${car.make} ${car.model}`} className="w-full h-40 object-cover"/>
            <div className="p-4">
                <h2 className="text-xl font-semibold">{car.make} {car.model}</h2>
                <p className="text-gray-600">Год: {car.year}</p>
                <p className="text-sm text-blue-600">Статус: {car.status}</p>
            </div>
        </Link>
    );
}