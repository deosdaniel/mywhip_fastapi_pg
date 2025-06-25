import {SquarePen} from "lucide-react"
import CarInfo from "@/components/CarInfo.jsx";

export default function CarDetails({car, onEdit}) {
    return (

        <div className="relative w-full">
            <div
                className="absolute -top-0 -right-0 flex gap-2 px-2 py-2 bg-color1 text-white rounded-md hover:bg-blue-700">
                <button
                    onClick={onEdit}
                    className=''>
                    <SquarePen/>
                </button>
            </div>
        </div>
    );
}
