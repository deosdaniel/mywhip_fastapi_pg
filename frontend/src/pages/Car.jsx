import {useEffect, useState} from "react";
import {useParams, useNavigate} from "react-router-dom";
import api from "../services/api";
import car_photo from "../assets/car_photo.jpg";
import IconAvito from "../assets/icons/avito.png"
import IconAutoru from "../assets/icons/autoru.webp"
import IconDrom from "../assets/icons/drom.png"
import IconAutoteka from "../assets/icons/autoteka.png"

// Статусы, аналог enum CarStatusChoices на фронте (пример)
const statuses = ["FRESH", "REPAIRING", "DETAILING", "LISTED", "SOLD"];

export default function Car() {
    const {car_uid} = useParams();
    const navigate = useNavigate();

    const [car, setCar] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({});

    const [expenses, setExpenses] = useState([]);
    const [expensesLoading, setExpensesLoading] = useState(true);
    const [expensesError, setExpensesError] = useState(null);

    useEffect(() => {
        const fetchCar = async () => {
            try {
                const res = await api.get(`/cars/${car_uid}`);
                setCar(res.data.result);
                setFormData(res.data.result);
            } catch (err) {
                console.error("Ошибка при загрузке машины:", err);
                setError("Не удалось загрузить данные машины.");
            } finally {
                setLoading(false);
            }
        };
        fetchCar();
    }, [car_uid]);

    useEffect(() => {
        const fetchExpenses = async () => {
            try {
                const res = await api.get(`/cars/${car_uid}/expenses`, {
                    params: {page: 1, limit: 100, sort_by: "created_at", order: "desc"}
                });
                setExpenses(res.data.result.content || []);
            } catch (err) {
                console.error("Ошибка при загрузке расходов:", err);
                setExpensesError("Не удалось загрузить расходы.");
            } finally {
                setExpensesLoading(false);
            }
        };
        fetchExpenses();
    }, [car_uid]);


    // Универсальная обработка изменений формы
    const handleChange = (e) => {
        const {name, value, type} = e.target;
        let val = value;

        // Если поле типа number, переводим в число или null
        if (type === "number") {
            val = value === "" ? "" : Number(value);
        }

        setFormData(prev => ({...prev, [name]: val}));
    };

    const handleSave = async () => {
        if (formData.price_purchased === "" || formData.price_purchased === undefined || isNaN(formData.price_purchased)) {
            alert("Пожалуйста, укажите цену покупки");
            return;
        }
        try {
            // Подготовим данные — уберём пустые строки, преобразуем числа
            const payload = {
                price_purchased: formData.price_purchased,
                date_listed: formData.date_listed === "" ? null : formData.date_listed,
                price_listed: formData.price_listed === "" ? null : +formData.price_listed,
                date_sold: formData.date_sold === "" ? null : formData.date_sold,
                price_sold: formData.price_sold === "" ? null : +formData.price_sold,
                autoteka_link: formData.autoteka_link === "" ? null : formData.autoteka_link,
                notes: formData.notes === "" ? null : formData.notes,
                avito_link: formData.avito_link === "" ? null : formData.avito_link,
                autoru_link: formData.autoru_link === "" ? null : formData.autoru_link,
                drom_link: formData.drom_link === "" ? null : formData.drom_link,
                status: formData.status === "" ? null : formData.status,
            };

            const res = await api.patch(`/cars/${car_uid}`, payload);
            setCar(res.data.result);
            setEditMode(false);
            alert("Данные успешно обновлены!");
        } catch (error) {
            console.error("Error while updating car", error);
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
            <div className="p-4 max-w-2xl mx-auto bg-white shadow-md rounded-lg ">
                <button onClick={() => navigate(-1)} className="mb-4 text-blue-600 hover:underline">
                    ← Назад
                </button>

                <div className='w-100 shadow-md rounded-md overflow-hidden mb-4'>
                    <img src={car_photo} alt={`${car.make} ${car.model}`} className="object-contain"/>
                </div>

                <h1 className="text-2xl font-bold mb-2">
                    {car.make} {car.model} ({car.year})
                </h1>

                {editMode ? (
                    <>
                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Статус:</label>
                            <select
                                name="status"
                                value={formData.status || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            >
                                <option value="" disabled>Выберите статус</option>
                                {statuses.map((status) => (
                                    <option key={status} value={status}>
                                        {status}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Цена покупки:</label>
                            <input
                                type="number"
                                name="price_purchased"
                                value={formData.price_purchased || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Дата выставления на продажу:</label>
                            <input
                                type="date"
                                name="date_listed"
                                value={formData.date_listed || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Цена выставления на продажу:</label>
                            <input
                                type="number"
                                name="price_listed"
                                value={formData.price_listed || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Дата продажи:</label>
                            <input
                                type="date"
                                name="date_sold"
                                value={formData.date_sold || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Цена продажи:</label>
                            <input
                                type="number"
                                name="price_sold"
                                value={formData.price_sold || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Ссылка на Автотеку:</label>
                            <input
                                type="text"
                                name="autoteka_link"
                                value={formData.autoteka_link || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Ссылка на Avito:</label>
                            <input
                                type="text"
                                name="avito_link"
                                value={formData.avito_link || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Ссылка на Auto.ru:</label>
                            <input
                                type="text"
                                name="autoru_link"
                                value={formData.autoru_link || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Ссылка на Drom:</label>
                            <input
                                type="text"
                                name="drom_link"
                                value={formData.drom_link || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                            />
                        </div>

                        <div className="mb-2">
                            <label className="block text-sm font-semibold">Заметки:</label>
                            <textarea
                                name="notes"
                                value={formData.notes || ""}
                                onChange={handleChange}
                                className="w-full border rounded px-2 py-1"
                                rows={4}
                            />
                        </div>


                        <div className="flex gap-2 mt-4">
                            <button
                                onClick={handleSave}
                                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                            >
                                Сохранить
                            </button>
                            <button
                                onClick={() => setEditMode(false)}
                                className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
                            >
                                Отмена
                            </button>
                        </div>
                    </>
                ) : (
                    <>
                        {/* Текущий вывод данных - оставим как есть */}
                        <p className="text-gray-600 mb-1"><strong>Статус:</strong> {car.status}</p>
                        <p className="text-gray-600 mb-1"><strong>VIN:</strong> {car.vin}</p>
                        <p className="text-gray-600 mb-1"><strong>ПТС:</strong> {car.pts_num}</p>
                        <p className="text-gray-600 mb-1"><strong>СТС:</strong> {car.sts_num}</p>
                        <p className="text-gray-600 mb-1"><strong>Дата покупки:</strong> {car.date_purchased}</p>
                        <p className="text-gray-600 mb-1"><strong>Цена
                            покупки:</strong> {car.price_purchased?.toLocaleString()} ₽</p>
                        {car.date_listed && (<p className="text-gray-600 mb-1"><strong>Дата выставления на
                            продажу:</strong> {car.date_listed}</p>)}
                        {car.price_listed && (<p className="text-gray-600 mb-1"><strong>Цена выставления на
                            продажу:</strong> {car.price_listed?.toLocaleString()} ₽</p>)}
                        {car.date_sold && (
                            <p className="text-gray-600 mb-1"><strong>Дата продажи:</strong> {car.date_sold}</p>)}
                        {car.price_sold && (<p className="text-gray-600 mb-1"><strong>Цена
                            продажи:</strong> {car.price_sold?.toLocaleString()} ₽</p>)}


                        <div>

                            {car.autoteka_link && (
                                <div className="flex gap-x-2">
                                    <img src={IconAutoteka} alt="avito" className="h-5 rounded-sm"/>
                                    <a href={car.autoteka_link} target="_blank" rel="noopener noreferrer"
                                       className="text-blue-500 hover:underline block">Отчет Автотеки</a>
                                </div>
                            )}

                            <div className="mt-2">Объявление</div>
                            <div className="flex justify-between mt-2">
                                {car.avito_link && (
                                    <div className="flex gap-x-2">
                                        <img src={IconAvito} alt="avito" className="h-5"/>
                                        <a href={car.avito_link} target="_blank" rel="noopener noreferrer"
                                           className="text-blue-500 hover:underline block">Avito</a>
                                    </div>
                                )}
                                {car.autoru_link && (
                                    <div className="flex gap-x-2">
                                        <img src={IconAutoru} alt="avito" className="h-5"/>
                                        <a href={car.autoru_link} target="_blank" rel="noopener noreferrer"
                                           className="text-blue-500 hover:underline block">Auto.ru</a>
                                    </div>
                                )}

                                {car.drom_link && (
                                    <div className="flex gap-x-2">
                                        <img src={IconDrom} alt="avito" className="h-5"/>
                                        <a href={car.drom_link} target="_blank" rel="noopener noreferrer"
                                           className="text-blue-500 hover:underline block">
                                            <div>Drom</div>
                                        </a>
                                    </div>
                                )}
                            </div>

                            {car.notes && (
                                <div>

                                    <div className="mt-2 p-2 bg-gray-50 rounded border">
                                        <div>Заметки</div>
                                        <p className="text-sm text-gray-700 whitespace-pre-wrap">{car.notes}</p>
                                    </div>
                                </div>
                            )}
                        </div>
                        <div className="mt-8">
                            <h2 className="text-xl font-bold mb-2">Расходы</h2>

                            {expensesLoading ? (
                                <p>Загрузка расходов...</p>
                            ) : expenses.length === 0 ? (
                                <p className="text-gray-500">Расходов пока нет.</p>
                            ) : (
                                <div className="overflow-x-auto">
                                    <table className="min-w-full bg-white border border-gray-300 text-sm">
                                        <thead className="bg-gray-100">
                                        <tr>
                                            <th className="px-3 py-2 border">№</th>
                                            <th className="px-3 py-2 border text-left">Название</th>
                                            <th className="px-3 py-2 border text-right">Сумма</th>
                                            <th className="px-3 py-2 border">Дата</th>
                                            <th className="px-3 py-2 border">Пользователь</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {expenses.map((exp, idx) => (
                                            <tr key={exp.uid} className="hover:bg-gray-50">
                                                <td className="px-3 py-2 border text-center">{idx + 1}</td>
                                                <td className="px-3 py-2 border">{exp.name}</td>
                                                <td className="px-3 py-2 border text-right">{exp.exp_summ.toLocaleString()} ₽</td>
                                                <td className="px-3 py-2 border text-center">
                                                    {new Date(exp.created_at).toLocaleDateString()}
                                                </td>
                                                <td className="px-3 py-2 border text-center">
                                                    {exp.user_uid || "-"}
                                                </td>
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                        <button
                            onClick={() => setEditMode(true)}
                            className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                        >
                            Редактировать
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}