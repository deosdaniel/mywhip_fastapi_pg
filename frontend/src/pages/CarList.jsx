import {Link} from "react-router-dom";
import CarCard from "../components/CarCard.jsx"
import carImg from "../assets/car_poster.jpg"

export default function CarsList() {
    const cars = [
        {
            id: 1,
            make: "Toyota",
            model: "Camry",
            year: 2015,
            status: "в продаже",
            image: carImg
        },
        {
            id: 2,
            make: "BMW",
            model: "X5",
            year: 2018,
            status: "продан",
            image: carImg
        }
    ];
    return (
        <div className='p-4'>
            <div className='flex justify-between items-center mb-4'>
                <h1 className='text-2xl font-bold'>Мои автомобили</h1>
                <Link to='app/cars/new ' className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                    + Добавить автомобиль
                </Link>
            </div>
            <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4'>
                {cars.map((car) => (
                    <CarCard key={car.id} car={car}/>
                ))}
            </div>
        </div>
    );
}