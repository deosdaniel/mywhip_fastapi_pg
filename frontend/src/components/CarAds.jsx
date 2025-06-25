import IconAvito from "@/assets/icons/avito.png";
import IconAutoru from "@/assets/icons/autoru.webp";
import IconDrom from "@/assets/icons/drom.png";

export default function CarAds({car, className}) {
    return (
        <div className={className}>
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
        </div>
    )
}