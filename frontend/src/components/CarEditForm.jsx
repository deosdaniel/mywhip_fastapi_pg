export default function CarEditForm({formData, setFormData, onSave, onCancel, statuses}) {
    const handleChange = (e) => {
        const {name, value, type} = e.target;
        let val = value;
        if (type === "number") val = value === "" ? "" : Number(value);
        setFormData(prev => ({...prev, [name]: val}));
    };

    const handleSubmit = () => {
        if (!formData.price_purchased) {
            alert("Укажите цену покупки");
            return;
        }

        const payload = {
            price_purchased: formData.price_purchased,
            date_listed: formData.date_listed || null,
            price_listed: formData.price_listed || null,
            date_sold: formData.date_sold || null,
            price_sold: formData.price_sold || null,
            autoteka_link: formData.autoteka_link || null,
            notes: formData.notes || null,
            avito_link: formData.avito_link || null,
            autoru_link: formData.autoru_link || null,
            drom_link: formData.drom_link || null,
            status: formData.status || null,
        };

        onSave(payload);
    };

    return (
        <div>
            <div className="mb-2">
                <label className="block text-sm font-semibold">Статус:</label>
                <select name="status" value={formData.status || ""} onChange={handleChange}
                        className="w-full border rounded px-2 py-1">
                    <option value="" disabled>Выберите статус</option>
                    {statuses.map(status => <option key={status} value={status}>{status}</option>)}
                </select>
            </div>

            <div className="mb-2">
                <label className="block text-sm font-semibold">Цена покупки:</label>
                <input type="number" name="price_purchased" value={formData.price_purchased || ""}
                       onChange={handleChange} className="w-full border rounded px-2 py-1"/>
            </div>

            {["date_listed", "price_listed", "date_sold", "price_sold"].map(field => (
                <div key={field} className="mb-2">
                    <label className="block text-sm font-semibold">{field.replace("_", " ")}:</label>
                    <input type={field.includes("date") ? "date" : "number"}
                           name={field}
                           value={formData[field] || ""}
                           onChange={handleChange}
                           className="w-full border rounded px-2 py-1"/>
                </div>
            ))}

            {["autoteka_link", "avito_link", "autoru_link", "drom_link"].map(field => (
                <div key={field} className="mb-2">
                    <label className="block text-sm font-semibold">{field.replace("_", " ")}:</label>
                    <input type="text" name={field} value={formData[field] || ""} onChange={handleChange}
                           className="w-full border rounded px-2 py-1"/>
                </div>
            ))}

            <div className="mb-2">
                <label className="block text-sm font-semibold">Заметки:</label>
                <textarea name="notes" value={formData.notes || ""} onChange={handleChange}
                          className="w-full border rounded px-2 py-1" rows={4}/>
            </div>

            <div className="flex gap-2 mt-4">
                <button onClick={handleSubmit} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                    Сохранить
                </button>
                <button onClick={onCancel} className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
                    Отмена
                </button>
            </div>
        </div>
    );
}
