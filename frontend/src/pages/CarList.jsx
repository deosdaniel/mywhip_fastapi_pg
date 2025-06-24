import {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import CarCard from "../components/CarCard.jsx";
import api from "../services/api";
import {Button} from "@/components/ui/button";
import {
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationPrevious,
    PaginationLink,
    PaginationNext,
} from "@/components/ui/pagination";

export default function CarsList() {
    const [cars, setCars] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const limit = 5; // Количество элементов на странице


    useEffect(() => {
        const fetchCars = async () => {
            try {
                const res = await api.get(`/cars/my_cars?page=${currentPage}&limit=${limit}&sort_by=created_at&order=desc`);
                setCars(res.data.result.content);
                setCars(res.data.result.content);
                setTotalPages(res.data.result.total_pages);
            } catch (err) {
                console.error("Error while fetching my cars data: ", err);
                setError("Failed to load my cars");
            } finally {
                setLoading(false);
            }
        };
        fetchCars();
    }, [currentPage]);
    const handlePageChange = (page) => {
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
        }
    };


    if (loading) {
        return <div className="p-4">Загружаю карточки автомобилей...</div>;
    }
    if (error) {
        return <div className="p-4 text-red-600">{error}</div>;
    }

    return (
        <div className="px-8 md:px-36">
            <div className="flex justify-between items-center  py-4">
                <h1 className="text-2xl font-bold">Мой сток</h1>
                <Button className="">
                    <Link to="new">+ Добавить</Link>
                </Button>

            </div>
            {cars.length === 0 ? (
                <p>У вас пока нет машин.</p>
            ) : (
                <>
                    <div className=" grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {cars.map((car) => (
                            <CarCard key={car.uid} car={car}/>
                        ))}
                    </div>
                    <div className="mt-8 flex justify-center">
                        <Pagination>
                            <PaginationContent>
                                <PaginationItem>
                                    <PaginationPrevious
                                        onClick={() => handlePageChange(currentPage - 1)}
                                        disabled={currentPage === 1}
                                    />
                                </PaginationItem>

                                {Array.from({length: totalPages}, (_, i) => i + 1).map(page => (
                                    <PaginationItem key={page}>
                                        <PaginationLink
                                            isActive={page === currentPage}
                                            onClick={() => handlePageChange(page)}
                                        >
                                            {page}
                                        </PaginationLink>
                                    </PaginationItem>
                                ))}

                                <PaginationItem>
                                    <PaginationNext
                                        onClick={() => handlePageChange(currentPage + 1)}
                                        disabled={currentPage === totalPages}
                                    />
                                </PaginationItem>
                            </PaginationContent>
                        </Pagination>
                    </div>
                </>
            )}
        </div>
    );
}
