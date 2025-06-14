
import car_poster from '../assets/car_poster.jpg'


function CarCard({car}) {
    function onFavoriteClick(){
        alert("clicked")
    }

    return <div className="car-card">
        <div className="car-poster">
            <img src={car_poster} alt={car.model} />
            <div className="car-overlay">
                <button className="favorite-btn" onClick={onFavoriteClick}>
                    BTN
                </button>
            </div>
        </div>
        <div className="car-info">
            <h3>{car.make} {car.model}</h3>
            <p>{car.year}</p>
        </div>
    </div>
}

export default CarCard