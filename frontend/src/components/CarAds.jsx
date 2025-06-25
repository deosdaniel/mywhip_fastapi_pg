import IconAvito from "@/assets/icons/avito.png";
import IconAutoru from "@/assets/icons/autoru.webp";
import IconDrom from "@/assets/icons/drom.png";
import {Button} from "@/components/ui/button.jsx";
import {NavLink} from "react-router-dom";

export default function CarAds({car, className}) {
    return (
        <div className={className}>
            <div className="flex justify-between">
                <Button>
                    <a href={car.avito_link} target="_blank" rel="noopener noreferrer">Avito</a>
                </Button>
                <Button>
                    <a href={car.autoru_link} target="_blank" rel="noopener noreferrer">Auto.ru</a>
                </Button>
                <Button>
                    <a href={car.drom_link} target="_blank" rel="noopener noreferrer">Drom</a>
                </Button>
            </div>
        </div>
    )
}