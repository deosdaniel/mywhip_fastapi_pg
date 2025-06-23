import {useEffect, useState} from "react";
import {useParams, useNavigate} from "react-router-dom";
import api from "../services/api";
import car_photo from "../assets/car_photo.jpg";
import CarEditForm from "../components/CarEditForm";
import CarDetails from "../components/CarDetails";
import ExpenseTable from "../components/ExpenseTable";
import NewExpenseModal from "../components/NewExpenseModal";

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
    const [showExpenseModal, setShowExpenseModal] = useState(false);
    const [newExpense, setNewExpense] = useState({name: "", exp_summ: ""});

    useEffect(() => {
        const fetchCar = async () => {
            try {
                const res = await api.get(`/cars/${car_uid}`);
                setCar(res.data.result);
                setFormData(res.data.result);
            } catch (err) {
                console.error("Error while fetching car data:", err);
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
                    params: {page: 1, limit: 100, sort_by: "created_at", order: "desc"},
                });
                setExpenses(res.data.result.content || []);
            } catch (err) {
                console.error("Error while fetching expense data:", err);
                setExpensesError("Не удалось загрузить расходы.");
            } finally {
                setExpensesLoading(false);
            }
        };
        fetchExpenses();
    }, [car_uid]);

    const handleUpdate = async (payload) => {
        try {
            const res = await api.patch(`/cars/${car_uid}`, payload);
            setCar(res.data.result);
            setEditMode(false);
            alert("Данные успешно обновлены!");
        } catch (error) {
            console.error("Error while updating car data:", error);
            const details = error.response?.data?.detail;
            if (Array.isArray(details)) {
                const messages = details.map((err, idx) => `${idx + 1}) ${err.msg}`).join("\n");
                alert(`Ошибки валидации:\n${messages}`);
            } else {
                alert(`Ошибка валидации: ${details || "Неизвестная ошибка"}`);
            }
        }
    };

    const handleDeleteExpense = async (expense_uid) => {
        if (!window.confirm("Вы уверены, что хотите удалить это вложение?")) return;

        try {
            await api.delete(`/cars/${car_uid}/expenses/${expense_uid}`);
            setExpenses((prev) => prev.filter((exp) => exp.uid !== expense_uid));
        } catch (err) {
            console.error("Error while deleting expense:", err);
            alert("Не удалось удалить расход.");
        }
    };

    const handleAddExpense = async () => {
        if (!newExpense.name || !newExpense.exp_summ) {
            alert("Заполните все поля!");
            return;
        }
        try {
            await api.post(`/cars/${car_uid}`, {
                name: newExpense.name,
                exp_summ: Number(newExpense.exp_summ),
            });
            setShowExpenseModal(false);
            setNewExpense({name: "", exp_summ: ""});
            const res = await api.get(`/cars/${car_uid}/expenses`, {
                params: {page: 1, limit: 100, sort_by: "created_at", order: "desc"},
            });
            setExpenses(res.data.result.content || []);
        } catch (err) {
            console.error("Error while creating expense:", err)
            const details = err.response?.data?.detail;
            if (Array.isArray(details)) {
                const messages = details.map((err, idx) => `${idx + 1}) ${err.msg}`).join("\n");
                alert(`Ошибки валидации:\n${messages}`);
            } else {
                alert(`Ошибка валидации: ${details || "Неизвестная ошибка"}`);
            }
        }
    };

    if (loading) return <div className="p-4">Загрузка...</div>;
    if (error) return <div className="p-4 text-red-600">{error}</div>;
    if (!car) return null;

    return (
        <div className="p-4">
            <h1 className="text-text text-2xl font-bold mb-4">Карточка автомобиля</h1>
            <div className="p-4 w-full bg-white shadow-md rounded-lg ">
                <button onClick={() => navigate(-1)} className="mb-4 text-primary hover:underline">
                    ← Назад
                </button>
                <img src={car_photo} alt="car" className="w-auto mb-4 rounded object-contain"/>

                <h2 className="text-2xl text-text font-bold mb-2">
                    {car.make} {car.model} ({car.year})
                </h2>

                {editMode ? (
                    <CarEditForm
                        formData={formData}
                        setFormData={setFormData}
                        onSave={handleUpdate}
                        onCancel={() => setEditMode(false)}
                        statuses={statuses}
                    />
                ) : (
                    <CarDetails car={car} onEdit={() => setEditMode(true)}/>
                )}

                <div className="mt-8">
                    <div className="flex justify-between items-center mb-2">
                        <h2 className="text-xl font-bold">Расходы</h2>
                        <button
                            onClick={() => setShowExpenseModal(true)}
                            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                        >
                            + Добавить расход
                        </button>
                    </div>
                    <ExpenseTable
                        expenses={expenses}
                        loading={expensesLoading}
                        error={expensesError}
                        onDelete={handleDeleteExpense}
                    />
                </div>
            </div>
            {showExpenseModal && (
                <NewExpenseModal
                    newExpense={newExpense}
                    setNewExpense={setNewExpense}
                    onClose={() => setShowExpenseModal(false)}
                    onSubmit={handleAddExpense}
                />
            )}
        </div>
    );
}
