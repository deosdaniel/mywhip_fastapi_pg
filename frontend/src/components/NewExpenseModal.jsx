export default function NewExpenseModal({newExpense, setNewExpense, onClose, onSubmit}) {
    const handleChange = (e) => {
        const {name, value} = e.target;
        setNewExpense(prev => ({...prev, [name]: value}));
    };

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-6 rounded-lg shadow-md max-w-md w-full">
                <h2 className="text-lg font-bold mb-4">Добавить расход</h2>

                <div className="mb-4">
                    <label className="block mb-1 font-semibold">Название:</label>
                    <input
                        type="text"
                        name="name"
                        value={newExpense.name}
                        onChange={handleChange}
                        className="w-full border px-3 py-2 rounded"
                    />
                </div>

                <div className="mb-4">
                    <label className="block mb-1 font-semibold">Сумма (₽):</label>
                    <input
                        type="number"
                        name="exp_summ"
                        value={newExpense.exp_summ}
                        onChange={handleChange}
                        className="w-full border px-3 py-2 rounded"
                    />
                </div>

                <div className="flex justify-end gap-2">
                    <button
                        onClick={onSubmit}
                        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                    >
                        Добавить
                    </button>
                    <button
                        onClick={onClose}
                        className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
                    >
                        Отмена
                    </button>
                </div>
            </div>
        </div>
    );
}
