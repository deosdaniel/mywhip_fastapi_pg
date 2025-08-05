import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogTrigger,
} from "@/components/ui/dialog";
import {Button} from "@/components/ui/button.jsx";

export default function NewExpenseModal({newExpense, setNewExpense, onClose, onSubmit, open, setOpen}) {
    const handleChange = (e) => {
        const {name, value} = e.target;
        setNewExpense(prev => ({...prev, [name]: value}));
    };

    
    const expTypeOptions = [
        {value: "PURCHASE", label: "Покупка авто"},
        {value: "PARTS", label: "Запчасти"},
        {value: "WHEELS", label: "Колеса/Шины"},
        {value: "REPAIR", label: "Работы по ремонту"},
        {value: "PAINT", label: "Покраска/Кузов"},
        {value: "FUEL", label: "Топливо"},
        {value: "DETAILING", label: "Подготовка"},
        {value: "ADS", label: "Объявление/продвижение"},
        {value: "OTHER", label: "Прочие расходы"},
    ]
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                    <DialogTitle>Добавить расход</DialogTitle>
                    <DialogDescription>
                        Заполните поля ниже для добавления нового вложения.
                    </DialogDescription>
                </DialogHeader>

                <div className="grid gap-4 py-4">
                    <div className="flex flex-col space-y-1">
                        <label htmlFor="type" className="font-semibold">Категория:</label>
                        <select
                            id="type"
                            name="type"
                            value={newExpense.type}
                            onChange={handleChange}
                            className="w-full rounded border border-input px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
                        >
                            <option value="" disabled>Выберите категорию</option>
                            {expTypeOptions.map(option => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="flex flex-col space-y-1">
                        <label htmlFor="name" className="font-semibold">Название:</label>
                        <input
                            id="name"
                            type="text"
                            name="name"
                            value={newExpense.name}
                            onChange={handleChange}
                            className="w-full rounded border border-input px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
                            autoComplete="off"
                        />
                    </div>

                    <div className="flex flex-col space-y-1">
                        <label htmlFor="exp_summ" className="font-semibold">Сумма (₽):</label>
                        <input
                            id="exp_summ"
                            type="number"
                            name="exp_summ"
                            value={newExpense.exp_summ}
                            onChange={handleChange}
                            className="w-full rounded border border-input px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
                            autoComplete="off"
                        />
                    </div>
                </div>

                <DialogFooter className="flex justify-end gap-2">
                    <Button variant="secondary" onClick={() => setOpen(false)}>
                        Отмена
                    </Button>
                    <Button onClick={onSubmit}>
                        Добавить
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}