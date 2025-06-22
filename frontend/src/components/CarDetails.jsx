import IconAvito from "../assets/icons/avito.png";
import IconAutoru from "../assets/icons/autoru.webp";
import IconDrom from "../assets/icons/drom.png";
import IconAutoteka from "../assets/icons/autoteka.png";

export default function CarDetails({car, onEdit}) {
    return (
        <div>
            <p className="text-gray-600 mb-1"><strong>Статус:</strong> {car.status}</p>
            <p className="text-gray-600 mb-1"><strong>VIN:</strong> {car.vin}</p>
            <p className="text-gray-600 mb-1"><strong>ПТС:</strong> {car.pts_num}</p>
            <p className="text-gray-600 mb-1"><strong>СТС:</strong> {car.sts_num}</p>
            <p className="text-gray-600 mb-1"><strong>Дата покупки:</strong> {car.date_purchased}</p>
            <p className="text-gray-600 mb-1"><strong>Цена покупки:</strong> {car.price_purchased?.toLocaleString()} ₽
            </p>

            {car.date_listed &&
                <p className="text-gray-600 mb-1"><strong>Дата выставления:</strong> {car.date_listed}</p>}
            {car.price_listed && <p className="text-gray-600 mb-1"><strong>Цена
                выставления:</strong> {car.price_listed?.toLocaleString()} ₽</p>}
            {car.date_sold && <p className="text-gray-600 mb-1"><strong>Дата продажи:</strong> {car.date_sold}</p>}
            {car.price_sold &&
                <p className="text-gray-600 mb-1"><strong>Цена продажи:</strong> {car.price_sold?.toLocaleString()} ₽
                </p>}

            <div className="mt-2">
                {car.autoteka_link && (
                    <div className="flex gap-x-2">
                        <img src={IconAutoteka} alt="autoteka" className="h-5 rounded-sm"/>
                        <a href={car.autoteka_link} target="_blank" rel="noopener noreferrer"
                           className="text-blue-500 hover:underline">Автотека</a>
                    </div>
                )}

                <div className="mt-2">Объявления</div>
                <div className="flex justify-between mt-2">
                    {car.avito_link && (
                        <div className="flex gap-x-2">
                            <img src={IconAvito} alt="avito" className="h-5"/>
                            <a href={car.avito_link} target="_blank" rel="noopener noreferrer"
                               className="text-blue-500 hover:underline">Avito</a>
                        </div>)
                    }
                    {car.autoru_link && (
                        <div className="flex gap-x-2">
                            <img src={IconAutoru} alt="autoru" className="h-5"/>
                            <a href={car.autoru_link} target="_blank" rel="noopener noreferrer"
                               className="text-blue-500 hover:underline">Auto.ru</a>
                        </div>)
                    }
                    {car.drom_link && (
                        <div className="flex gap-x-2">
                            <img src={IconDrom} alt="drom" className="h-5"/>
                            <a href={car.drom_link} target="_blank" rel="noopener noreferrer"
                               className="text-blue-500 hover:underline">Drom</a>
                        </div>)
                    }
                </div>

                {car.notes && (
                    <div className="mt-2 p-2 bg-gray-50 rounded border">
                        <div>Заметки</div>
                        <p className="text-sm text-gray-700 whitespace-pre-wrap">{car.notes}</p>
                    </div>
                )}
            </div>

            <button
                onClick={onEdit}
                className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Редактировать
            </button>
        </div>
    );
}
