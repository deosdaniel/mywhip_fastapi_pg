import {useState} from "react";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"


export default function CarOwnersStats({car, className}) {

    if (!car?.stats?.owners_stats) return <p>Загрузка информации…</p>;

    const owners = car.stats.owners_stats;

    return (
        <div className={className}>
            <div className="flex justify-between items-center mb-2">
                <h2 className="text-xl font-bold">Партнеры</h2>
            </div>
            <Table>
                <TableHeader className="bg-accent">
                    <TableRow>
                        <TableHead className="font-bold">№</TableHead>
                        <TableHead className="font-bold">Email</TableHead>
                        <TableHead className="font-bold">Никнейм</TableHead>
                        <TableHead className="font-bold">Вложения</TableHead>
                        <TableHead className="font-bold">Выплата</TableHead>
                        <TableHead></TableHead>
                    </TableRow>
                </TableHeader>
                {owners.length === 0 ? (
                    ""
                ) : (
                    <TableBody>
                        {owners.map((owner, idx) => (
                            <TableRow key={owner.owner_uid}>
                                <TableCell>{idx + 1}</TableCell>
                                <TableCell>{owner.email}</TableCell>
                                <TableCell>{owner.username}</TableCell>
                                <TableCell>{owner.owner_total_expenses.toLocaleString()} ₽</TableCell>
                                <TableCell>{owner.net_payout.toLocaleString()} ₽</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                )}
            </Table>
        </div>
    );
}