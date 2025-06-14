import CarCard from "../components/CarCard";


export default function Dashboard() {
    return(
    <>
        <CarCard car={{make: "Toyota", model:"Corolla", year: 2008}}/>
    </>
    );
}