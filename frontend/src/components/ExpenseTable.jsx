import {
    Table,
    TableBody,
    TableCaption,
    TableCell, TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {X} from "lucide-react"

export default function ExpenseTable({expenses, loading, error, onDelete, className}) {
    if (loading) return <p>Загрузка расходов...</p>;
    if (error) return <p className="text-red-600">{error}</p>;

    if (expenses.length === 0) {
        return <p className="text-gray-500">Расходов пока нет.</p>;
    }

    return (
        <div className={className}>
            <Table>
                <TableHeader className="bg-accent">
                    <TableRow>
                        <TableHead className="font-bold">№</TableHead>
                        <TableHead className="font-bold">Название</TableHead>
                        <TableHead className="font-bold">Сумма</TableHead>
                        <TableHead className="font-bold">Дата</TableHead>
                        {/*<TableHead className="">Пользователь</TableHead>*/}
                        <TableHead className=""></TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {expenses.map((exp, idx) => (
                        <TableRow key={exp.uid} className="">
                            <TableCell className="">{idx + 1}</TableCell>
                            <TableCell className="">{exp.name}</TableCell>
                            <TableCell
                                className="">{exp.exp_summ.toLocaleString()} ₽</TableCell>
                            <TableCell className="">
                                {new Date(exp.created_at).toLocaleDateString()}
                            </TableCell>
                            {/*<TableCell className="">
                                {exp.user?.email || "-"}
                            </TableCell>*/}
                            <TableCell className="">
                                <X
                                    onClick={() => onDelete(exp.uid)}
                                    className="text-red-700 cursor-pointer"
                                    title="Удалить"
                                >
                                </X>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TableCell colSpan={2} className="font-bold">Всего вложений:</TableCell>
                        <TableCell colSpan={3} className="">{10000} ₽</TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
        </div>
    );
}
