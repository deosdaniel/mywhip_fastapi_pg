import {useEffect, useState} from "react";
import {useParams, useNavigate} from "react-router-dom";
import api from "../services/api";
import car_photo from "../assets/car_photo.jpg";
import ExpenseTable from "../components/ExpenseTable";
import NewExpenseModal from "../components/NewExpenseModal";
import {Button} from "@/components/ui/button.jsx";
import {ChevronLeftIcon, SquarePen, Plus} from "lucide-react";
import CarInfo from "@/components/CarInfo.jsx";
import CarStats from "@/components/CarStats.jsx";
import CarAds from "@/components/CarAds.jsx";
import CarNotes from "@/components/CarNotes.jsx";
import EditCarModal from "@/components/EditCarModal.jsx";

const statuses = ["FRESH", "REPAIRING", "DETAILING", "LISTED", "SOLD"];

export default function Car() {
    const {car_uid} = useParams();
    const navigate = useNavigate();

    const [car, setCar] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({});


    useEffect(() => {
        const fetchCar = async () => {
            try {
                const res = await api.get(`/cars/${car_uid}`);
                setCar(res.data.result);
                setFormData(res.data.result);
            } catch (err) {
                console.error("Error while fetching car data:", err);
                setError("Не удалось загрузить данные машины.");
            } finally {
                setLoading(false);
            }
        };
        fetchCar();
    }, [car_uid]);


    const handleUpdate = async (payload) => {
        try {
            const res = await api.patch(`/cars/${car_uid}`, payload);
            setCar(res.data.result);
            setEditMode(false);
            alert("Данные успешно обновлены!");
        } catch (error) {
            console.error("Error while updating car data:", error);
            const details = error.response?.data?.detail;
            if (Array.isArray(details)) {
                const messages = details
                    .map((err, idx) => `${idx + 1}) ${err.msg}`)
                    .join("\n");
                alert(`Ошибки валидации:\n${messages}`);
            } else {
                alert(`Ошибка валидации: ${details || "Неизвестная ошибка"}`);
            }
        }
    };

    if (loading) return <div className="p-4">Загрузка...</div>;
    if (error) return <div className="p-4 text-red-600">{error}</div>;
    if (!car) return null;
    return (
        <div className="px-6 md:px-28 flex-col justify-center">
            <div className="flex items-center py-4 gap-4">
                <Button variant="secondary" size="icon" className="cursor-pointer size-8" onClick={() => navigate(-1)}>
                    <ChevronLeftIcon/>
                </Button>
                <h2 className="text-2xl text-text font-bold">
                    {car.make} {car.model} ({car.year})
                </h2>

            </div>
            <div className="w-full bg-white shadow-md rounded-lg overflow-hidden relative">
                <p className="absolute top-4 left-4 text-primary bg-green-200 py-1 px-4 rounded-md shadow">{car.status}</p>
                <Button variant="secondary" className="absolute top-4 right-4 cursor-pointer"
                        onClick={() => setEditMode(true)}>
                    <SquarePen className=""/>
                </Button>
                <img
                    src={car_photo}
                    alt="car"
                    className="w-full object-contain"
                />
            </div>

            <div>
                <div className="flex flex-col gap-2 py-2">

                    <CarInfo car={car} className="w-full grid md:grid-cols-2 bg-white shadow-md rounded-lg p-4"/>
                    <CarStats car={car} className="w-full grid md:grid-cols-2 bg-white shadow-md rounded-lg p-4"/>
                    <CarAds car={car} className="w-full bg-white shadow-md rounded-lg p-4"/>
                    <CarNotes car={car} className="w-full bg-white shadow-md rounded-lg p-4"/>
                    <ExpenseTable car_uid={car_uid} className="w-full bg-white shadow-md rounded-lg p-4"/>
                </div>

            </div>
            {editMode && (
                <EditCarModal
                    formData={formData}
                    setFormData={setFormData}
                    onSave={handleUpdate}
                    onClose={() => setEditMode(false)}
                    statuses={statuses}
                />
            )}
        </div>
    );
}
