import CarCard from "../components/CarCard";


export default function Dashboard() {
    return(
    <>
        <div>



            <CarCard car={{make: "Toyota", model:"Corolla", year: 2008}}/>
        </div>
    </>
    );
}