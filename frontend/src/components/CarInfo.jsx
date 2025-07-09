export default function CarInfo({car, className}) {
    return (
        <div className={className}>
            <p className="text-gray-600 mb-1"><strong>VIN:</strong> {car.vin}</p>
            <p className="text-gray-600 mb-1"><strong>ПТС:</strong> {car.pts_num}</p>
            <p className="text-gray-600 mb-1"><strong>СТС:</strong> {car.sts_num}</p>
            <div className="flex gap-x-2">
                <p className="text-gray-600 mb-1"><strong>Отчет Автотеки: </strong></p>
                <div className="flex gap-x-2">
                    <a href={car.autoteka_link} target="_blank" rel="noopener noreferrer"
                       className="text-blue-500 hover:underline">Cсылка</a>
                </div>
            </div>
        </div>
    );
}