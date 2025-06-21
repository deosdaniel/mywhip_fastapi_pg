import {useEffect, useState} from "react";
import {useParams, useNavigate} from "react-router-dom";
import api from "../services/api";
import car_photo from "../assets/car_photo.jpg";

export default function Car() {
    const {car_uid} = useParams(); // uid машины из URL
    const navigate = useNavigate();

    const [car, setCar] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCar = async () => {
            try {
                const res = await api.get(`/cars/${car_uid}`);
                setCar(res.data.result);
            } catch (err) {
                console.error("Ошибка при загрузке машины:", err);
                setError("Не удалось загрузить данные машины.");
            } finally {
                setLoading(false);
            }
        };

        fetchCar();
    }, [car_uid]);

    if (loading) return <div className="p-4">Загрузка...</div>;
    if (error) return <div className="p-4 text-red-600">{error}</div>;
    if (!car) return null;

    return (
        <div className="p-4">
            <h1 className='text-white text-2xl font-bold mb-4'>Карточка автомобиля</h1>
            <div className="p-4 max-w-2xl mx-auto bg-white shadow-md rounded-lg">

                <button
                    onClick={() => navigate(-1)}
                    className="mb-4 text-blue-600 hover:underline"
                >
                    ← Назад
                </button>
                <div className='w-100 shadow-md rounded-md overflow-hidden mb-4'>
                    <img src={car_photo} alt={`${car.make} ${car.model}`} className=" object-contain"/>
                </div>
                <h1 className="text-2xl font-bold mb-2">
                    {car.make} {car.model} ({car.year})
                </h1>

                <p className="text-gray-600 mb-1"><strong>VIN:</strong> {car.vin}</p>
                <p className="text-gray-600 mb-1"><strong>ПТС:</strong> {car.pts_num}</p>
                <p className="text-gray-600 mb-1"><strong>СТС:</strong> {car.sts_num}</p>
                <p className="text-gray-600 mb-1"><strong>Дата покупки:</strong> {car.date_purchased}</p>
                <p className="text-gray-600 mb-1"><strong>Цена
                    покупки:</strong> {car.price_purchased?.toLocaleString()} ₽
                </p>
                <p className="text-gray-600 mb-1"><strong>Статус:</strong> {car.status}</p>

                {/* Ссылки, если есть */}
                <div className="mt-4">
                    {car.autoteka_link && (
                        <a href={car.autoteka_link} target="_blank" rel="noopener noreferrer"
                           className="text-blue-500 hover:underline block">Автотека</a>
                    )}
                    {car.avito_link && (
                        <a href={car.avito_link} target="_blank" rel="noopener noreferrer"
                           className="text-blue-500 hover:underline block">Avito</a>
                    )}
                    {car.autoru_link && (
                        <a href={car.autoru_link} target="_blank" rel="noopener noreferrer"
                           className="text-blue-500 hover:underline block">Auto.ru</a>
                    )}
                    {car.drom_link && (
                        <a href={car.drom_link} target="_blank" rel="noopener noreferrer"
                           className="text-blue-500 hover:underline block">Drom</a>
                    )}
                </div>

                {car.notes && (
                    <div className="mt-4 p-2 bg-gray-50 rounded border">
                        <p className="text-sm text-gray-700 whitespace-pre-wrap">{car.notes}</p>
                    </div>
                )}
            </div>
        </div>
    );
}