import {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import CarCard from "../components/CarCard.jsx";
import api from "../services/api";
import carImg from "../assets/car_poster.jpg";

export default function CarsList() {
    const [cars, setCars] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCars = async () => {
            try {
                const res = await api.get('/cars/my_cars');
                setCars(res.data.result.content);
            } catch (err) {
                console.error("Error while fetching my cars data: ", err);
                setError("Failed to load my cars");
            } finally {
                setLoading(false);
            }
        };
        fetchCars();
    }, []);
    if (loading) {
        return <div className="p-4">Загружаю карточки автомобилей...</div>;
    }
    if (error) {
        return <div className="p-4 text-red-600">{error}</div>;
    }

    return (
        <div className='p-4'>
            <div className='flex justify-between text-white  mb-4'>
                <h1 className='text-2xl font-bold'>Мои автомобили</h1>
                <Link to='new'
                      className="inline-block mb-4 px-4 py-1 bg-green-600  rounded hover:bg-green-700">
                    + Добавить
                </Link>
            </div>
            {cars.length === 0 ? (
                <p>У вас пока нет машин.</p>
            ) : (
                <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4'>
                    {cars.map((car) => (
                        <CarCard key={car.uid} car={car}/>
                    ))}
                </div>
            )}
        </div>
    );
}