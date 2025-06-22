export default function ExpenseTable({expenses, loading, error, onDelete}) {
    if (loading) return <p>Загрузка расходов...</p>;
    if (error) return <p className="text-red-600">{error}</p>;

    if (expenses.length === 0) {
        return <p className="text-gray-500">Расходов пока нет.</p>;
    }

    return (
        <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-300 text-sm">
                <thead className="bg-gray-200">
                <tr>
                    <th className="px-3 py-2 border">№</th>
                    <th className="px-3 py-2 border text-left">Название</th>
                    <th className="px-3 py-2 border text-right">Сумма</th>
                    <th className="px-3 py-2 border">Дата</th>
                    <th className="px-3 py-2 border">Пользователь</th>
                    <th className="px-3 py-2 border text-center">Удалить</th>
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
                            {exp.user?.email || "-"}
                        </td>
                        <td className="px-3 py-2 border text-center">
                            <button
                                onClick={() => onDelete(exp.uid)}
                                className="text-red-600 hover:text-red-800"
                                title="Удалить расход"
                            >
                                ❌
                            </button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}
