export default function CarStats({car, className}) {
    return (
        <div className={className}>
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
        </div>
    )
}