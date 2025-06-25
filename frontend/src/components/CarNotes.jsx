export default function CarNotes({car, className}) {
    return (
        <div className={className}>

            <div className="mt-2 p-2 bg-gray-50 rounded border">
                <div>Заметки</div>
                <p className="text-sm text-gray-700 whitespace-pre-wrap">{car.notes}</p>
            </div>
        </div>
    )
}