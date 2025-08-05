import {useState} from "react";
import {useNavigate} from "react-router-dom";
import api from "../services/api";

export default function NewCarForm() {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        make: "",
        model: "",
        year: new Date().getFullYear(),
        vin: "",
        pts_num: "",
        sts_num: "",
        date_purchased: new Date().toISOString().split("T")[0],
        status: "FRESH"
    });
    const handleChange = (e) => {
        setForm({...form, [e.target.name]: e.target.value});
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem("token");
            await api.post("/cars", form, {
                headers: {Authorization: `Bearer ${token}`}

            });
            console.log("Car created successfully");

            alert(`Карточка автомобиля успешно создана! Ваш ${form.make} ${form.model} уже ждет личном кабинете! :)`);
            navigate("/app/cars");
        } catch (error) {
            console.error("Error while creating car", error);
            const details = error.response?.data?.detail;

            if (Array.isArray(details)) {
                const messages = details.map((err, idx) => `${idx + 1}) ${err.msg}`).join('\n');
                alert(`Ошибки валидации:\n${messages}`);
            } else {
                alert(`Произошла ошибка: ${details || 'Неизвестная ошибка'}`);
            }
        }
    };
    return (
        <div className="max-w-xs mx-auto mt-8 p-4 border rounded shadow">
            <h2 className='text-xl font-bold mb-4'>Добавить автомобиль</h2>
            <form onSubmit={handleSubmit} className='space-y-4'>
                <input name="make" value={form.make} onChange={handleChange} placeholder="Марка"
                       className='w-full p-2 border rounded' required/>
                <input name="model" value={form.model} onChange={handleChange} placeholder="Модель"
                       className='w-full p-2 border rounded' required/>
                <input name="year" value={form.year} onChange={handleChange} type="number"
                       placeholder="Год выпуска" className='w-full p-2 border rounded' required/>
                <input name="vin" value={form.vin} onChange={handleChange} placeholder="VIN-номер/Номер кузова"
                       className='w-full p-2 border rounded' required/>
                <input name="pts_num" value={form.pts_num} onChange={handleChange} placeholder="Серия и номер ПТС"
                       className='w-full p-2 border rounded' required/>
                <input name="sts_num" value={form.sts_num} onChange={handleChange} placeholder="Серия и номер СТС"
                       className='w-full p-2 border rounded' required/>
                <p>Дата покупки</p>
                <input name="date_purchased" value={form.date_purchased} onChange={handleChange} type="date"
                       className='w-full p-2 border rounded' required/>
                <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Сохранить</button>
            </form>
        </div>
    );
}