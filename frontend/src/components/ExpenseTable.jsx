import {useEffect, useState} from "react";
import {
    Table,
    TableBody,
    TableCell, TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {X, Plus} from "lucide-react"
import {Button} from "@/components/ui/button.jsx";
import api from "../services/api";
import NewExpenseModal from "./NewExpenseModal";

export default function ExpenseTable({car_uid, className}) {
    const [expenses, setExpenses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [showExpenseModal, setShowExpenseModal] = useState(false);
    const [newExpense, setNewExpense] = useState({name: "", exp_summ: ""});

    // Загрузка вложений
    useEffect(() => {
        const fetchExpenses = async () => {
            setLoading(true);
            setError(null);
            try {
                const res = await api.get(`/cars/${car_uid}/expenses`, {
                    params: {page: 1, limit: 100, sort_by: "created_at", order: "desc"},
                });
                setExpenses(res.data.result.content || []);
            } catch (err) {
                setError("Не удалось загрузить вложения.");
            } finally {
                setLoading(false);
            }
        };
        fetchExpenses();
    }, [car_uid]);

    const handleDelete = async (expense_uid) => {
        if (!window.confirm("Вы уверены, что хотите удалить это вложение?")) return;
        try {
            await api.delete(`/cars/${car_uid}/expenses/${expense_uid}`);
            setExpenses((prev) => prev.filter((exp) => exp.uid !== expense_uid));
        } catch (err) {
            alert("Не удалось удалить вложение.");
        }
    };

    const handleAddExpense = async () => {
        if (!newExpense.type || !newExpense.exp_summ) {
            alert("Заполните все поля!");
            return;
        }
        try {
            await api.post(`/cars/${car_uid}`, {
                type: newExpense.type,
                name: newExpense.name,
                exp_summ: Number(newExpense.exp_summ),
            });
            setShowExpenseModal(false);
            setNewExpense({type: "", name: "", exp_summ: ""});
            // Перезагрузка списка
            const res = await api.get(`/cars/${car_uid}/expenses`, {
                params: {page: 1, limit: 100, sort_by: "created_at", order: "desc"},
            });
            setExpenses(res.data.result.content || []);
        } catch (err) {
            const details = err.response?.data?.detail;
            if (Array.isArray(details)) {
                alert("Ошибки валидации:\n" + details.map((e, i) => `${i + 1}) ${e.msg}`).join("\n"));
            } else {
                alert(`Ошибка валидации: ${details || "Неизвестная ошибка"}`);
            }
        }
    };

    if (loading) return <p>Загрузка расходов...</p>;
    if (error) return <p className="text-red-600">{error}</p>;


    return (
        <div className={className}>
            <div className="flex justify-between items-center mb-2">
                <h2 className="text-xl font-bold">Вложения</h2>
                <Button onClick={() => setShowExpenseModal(true)} variant="secondary"
                        className="flex items-center gap-1">
                    <Plus/> Добавить
                </Button>
            </div>
            <Table>
                <TableHeader className="bg-accent">
                    <TableRow>
                        <TableHead className="font-bold">№</TableHead>
                        <TableHead className="font-bold">Категория</TableHead>
                        <TableHead className="font-bold">Сумма</TableHead>
                        <TableHead className="font-bold">Дата</TableHead>
                        <TableHead className="font-bold">Автор</TableHead>
                        <TableHead></TableHead>
                    </TableRow>
                </TableHeader>
                {expenses.length === 0 ? (
                    ""
                ) : (
                    <TableBody>
                        {expenses.map((exp, idx) => (
                            <TableRow key={exp.uid}>
                                <TableCell>{idx + 1}</TableCell>
                                <TableCell>{exp.type}</TableCell>
                                <TableCell>{exp.exp_summ.toLocaleString()} ₽</TableCell>
                                <TableCell>{new Date(exp.created_at).toLocaleDateString()}</TableCell>
                                <TableCell>{exp.user.email.toLocaleString()}</TableCell>
                                <TableCell>
                                    <X
                                        onClick={() => handleDelete(exp.uid)}
                                        className="text-red-700 cursor-pointer"
                                        title="Удалить"
                                    />
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                )}
                <TableFooter>
                    <TableRow>
                        <TableCell colSpan={2} className="font-bold">Всего вложений:</TableCell>
                        <TableCell colSpan={3}>
                            {expenses.reduce((acc, e) => acc + e.exp_summ, 0).toLocaleString()} ₽
                        </TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
            <NewExpenseModal
                newExpense={newExpense}
                setNewExpense={setNewExpense}
                open={showExpenseModal}
                setOpen={setShowExpenseModal}
                onClose={() => setShowExpenseModal(false)}
                onSubmit={handleAddExpense}
            />
        </div>
    );
}