import {Input} from "@/components/ui/input";
import {Textarea} from "@/components/ui/textarea";
import {Button} from "@/components/ui/button";
import {Label} from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";

export default function CarEditForm({formData, setFormData, onSave, onCancel, statuses}) {
    const handleChange = (e) => {
        const {name, value, type} = e.target;
        let val = value;
        if (type === "number") val = value === "" ? "" : Number(value);
        setFormData(prev => ({...prev, [name]: val}));
    };

    const handleSelectChange = (value) => {
        setFormData(prev => ({...prev, status: value}));
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
        <div className="space-y-4">
            <div>
                <Label>Статус</Label>
                <Select value={formData.status || ""} onValueChange={handleSelectChange}>
                    <SelectTrigger>
                        <SelectValue placeholder="Выберите статус"/>
                    </SelectTrigger>
                    <SelectContent>
                        {statuses.map(status => (
                            <SelectItem key={status} value={status}>
                                {status}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            <div>
                <Label>Цена покупки</Label>
                <Input
                    type="number"
                    name="price_purchased"
                    value={formData.price_purchased || ""}
                    onChange={handleChange}
                />
            </div>

            {["date_listed", "price_listed", "date_sold", "price_sold"].map((field) => (
                <div key={field}>
                    <Label>{field.replace("_", " ")}</Label>
                    <Input
                        type={field.includes("date") ? "date" : "number"}
                        name={field}
                        value={formData[field] || ""}
                        onChange={handleChange}
                    />
                </div>
            ))}

            {["autoteka_link", "avito_link", "autoru_link", "drom_link"].map((field) => (
                <div key={field}>
                    <Label>{field.replace("_", " ")}</Label>
                    <Input
                        type="text"
                        name={field}
                        value={formData[field] || ""}
                        onChange={handleChange}
                    />
                </div>
            ))}

            <div>
                <Label>Заметки</Label>
                <Textarea
                    name="notes"
                    value={formData.notes || ""}
                    onChange={handleChange}
                    rows={4}
                />
            </div>

            <div className="flex justify-end gap-2 pt-2">
                <Button variant="secondary" onClick={onCancel}>
                    Отмена
                </Button>
                <Button onClick={handleSubmit}>
                    Сохранить
                </Button>
            </div>
        </div>
    );
}