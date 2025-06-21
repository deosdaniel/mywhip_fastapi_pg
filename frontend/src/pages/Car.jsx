import {useEffect, useState} from "react";
import {useParams, useNavigate} from "react-router-dom";
import api from "../services/api";
import car_photo from "../assets/car_photo.jpg";

export default function Car() {
    const {car_uid} = useParams();
    const navigate = useNavigate();

    const [car, setCar] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({});

    useEffect(() => {
        const fetchCar = async () => {
            try {
                const res = await api.get(`/cars/${car_uid}`);
                setCar(res.data.result);
                setFormData(res.data.result); // инициализируем форму
            } catch (err) {
                console.error("Ошибка при загрузке машины:", err);
                setError("Не удалось загрузить данные машины.");
            } finally {
                setLoading(false);
            }
        };

        fetchCar();
    }, [car_uid]);

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };

    const handleSave = async () => {
        try {
            const payload = {
                ...formData,
                price_purchased: formData.price_purchased ? +formData.price_purchased : undefined,
                price_listed: formData.price_listed ? +formData.price_listed : undefined,
                price_sold: formData.price_sold ? +formData.price_sold : undefined,
            };
            const res = await api.patch(`/cars/${car_uid}`, payload);
            setCar(res.data.result);
            setEditMode(false);
            console.log("Data updated successfully", res.data);

            alert(`Данные успешно обновлены!`);

        } catch (e) {
            console.error("Error while creating car", error);
            const details = error.response?.data?.detail;

            if (Array.isArray(details)) {
                const messages = details.map((err, idx) => `${idx + 1}) ${err.msg}`).join('\n');
                alert(`Ошибки валидации:\n${messages}`);
            } else {
                alert(`Ошибка валидации: ${details || 'Неизвестная ошибка'}`);
            }
        }
    };

    if (loading) return <div className="p-4">Загрузка...</div>;
    if (error) return <div className="p-4 text-red-600">{error}</div>;
    if (!car) return null;

    return (
        <div className="p-4">
            <h1 className='text-white text-2xl font-bold mb-4'>Карточка автомобиля</h1>
            <div className="p-4 max-w-2xl mx-auto bg-white shadow-md rounded-lg">
                <button onClick={() => navigate(-1)} className="mb-4 text-blue-600 hover:underline">
                    ← Назад
                </button>

                <div className='w-100 shadow-md rounded-md overflow-hidden mb-4'>
                    <img src={car_photo} alt={`${car.make} ${car.model}`} className=" object-contain"/>
                </div>

                <h1 className="text-2xl font-bold mb-2">
                    {car.make} {car.model} ({car.year})
                </h1>

                {editMode ? (
                    <>
                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Цена покупки:</label>
                            <input type="number" name="price_purchased" value={formData.price_purchased || ""}
                                   onChange={handleChange}
                                   className="w-full border rounded px-2 py-1"/>
                        </div>
                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Ссылка на Автотеку:</label>
                            <input type="text" name="autoteka_link" value={formData.autoteka_link || ""}
                                   onChange={handleChange}
                                   className="w-full border rounded px-2 py-1"/>
                        </div>
                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Заметки:</label>
                            <textarea name="notes" value={formData.notes || ""} onChange={handleChange}
                                      className="w-full border rounded px-2 py-1" rows={4}/>
                        </div>
                        <div className="flex gap-2 mt-4">
                            <button onClick={handleSave}
                                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                                Сохранить
                            </button>
                            <button onClick={() => setEditMode(false)}
                                    className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
                                Отмена
                            </button>
                        </div>
                    </>
                ) : (
                    <>
                        <p className="text-gray-600 mb-1"><strong>VIN:</strong> {car.vin}</p>
                        <p className="text-gray-600 mb-1"><strong>ПТС:</strong> {car.pts_num}</p>
                        <p className="text-gray-600 mb-1"><strong>СТС:</strong> {car.sts_num}</p>
                        <p className="text-gray-600 mb-1"><strong>Дата покупки:</strong> {car.date_purchased}</p>
                        <p className="text-gray-600 mb-1"><strong>Цена
                            покупки:</strong> {car.price_purchased?.toLocaleString()} ₽</p>
                        <p className="text-gray-600 mb-1"><strong>Статус:</strong> {car.status}</p>

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

                        <button onClick={() => setEditMode(true)}
                                className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                            Редактировать
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}