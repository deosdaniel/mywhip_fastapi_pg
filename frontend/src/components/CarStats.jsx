function formatPrice(price) {
    return price && price !== 0 ? price.toLocaleString() + ' ₽' : '–';
}

function formatPercent(price) {
    return price && price !== 0 ? price.toLocaleString() + ' %' : '–';
}

export default function CarStats({car, className}) {
    if (!car?.stats) return <p className={className}>Загрузка...</p>;
    return (
        <div className={className}>
            <p className="text-gray-600 mb-1"><strong>Дата покупки:</strong> {car.date_purchased}</p>
            <p className="text-gray-600 mb-1"><strong>Цена покупки:
            </strong> {formatPrice(car.stats.pri1ce_purchased)}
            </p>
            <p className="text-gray-600 mb-1"><strong>
                Сумма вложений:</strong> {formatPrice(car.stats.total_expenses)}
            </p>
            <p className="text-gray-600 mb-1">
                <strong>Себестоимость:</strong> {formatPrice(car.stats.total_cost)}
            </p>

            <p className="text-gray-600 mb-1"><strong>Дата выставления:</strong> {car.date_listed ?? '–'}</p>
            <p className="text-gray-600 mb-1"><strong>Цена выставления:</strong> {formatPrice(car.price_listed)}
            </p>
            <p className="text-gray-600 mb-1"><strong>Потен.
                прибыль:</strong> {formatPrice(car.stats.potential_profit)}
            </p>
            <p className="text-gray-600 mb-1"><strong>Потенц.
                маржинальность:</strong> {formatPercent(car.stats.potential_margin)}
            </p>
            <p className="text-gray-600 mb-1"><strong>Дата продажи:</strong> {car.date_sold ?? '–'}</p>
            <p className="text-gray-600 mb-1"><strong>Цена продажи:</strong> {formatPrice(car.price_sold)}
            </p>
            <p className="text-gray-600 mb-1"><strong>Прибыль:</strong> {formatPrice(car.stats.profit)}
            </p>
            <p className="text-gray-600 mb-1"><strong>Маржинальность:</strong> {formatPercent(car.stats.margin)}
            </p>


        </div>
    )
}