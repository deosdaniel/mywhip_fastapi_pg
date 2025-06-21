import {BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom";
import Login from './pages/Login';
import ProfileEdit from "./pages/ProfileEdit.jsx";
import ProtectedRoute from "./components/ProtectedRoute";
import PublicRoute from "./components/PublicRoute.jsx";
import Signup from "./pages/Signup";
import Home from "./pages/Home.jsx";
import AppLayout from "./pages/AppLayout.jsx";
import CarsList from "./pages/CarList.jsx";
import Car from "./pages/Car.jsx";
import Profile from "./pages/Profile.jsx";
import NotFound from "./pages/NotFound.jsx";
import NewCarForm from "./pages/NewCarForm.jsx";

function App() {
    return (
        <div className="App">
            <Router>
                <Routes>
                    <Route path="/" element={<PublicRoute><Home/></PublicRoute>}/>
                    <Route path="/login" element={<PublicRoute><Login/></PublicRoute>}/>
                    <Route path="/signup" element={<PublicRoute><Signup/></PublicRoute>}/>

                    <Route path="/app" element={<ProtectedRoute><AppLayout/></ProtectedRoute>}>
                        <Route index element={<Navigate to="cars"/>}/>
                        <Route path="cars" element={<CarsList/>}/>
                        <Route path="cars/new" element={<NewCarForm/>}/>
                        <Route path="cars/:car_uid" element={<Car/>}/>
                        <Route path="profile" element={<Profile/>}/>
                        <Route path="profile/edit" element={<ProfileEdit/>}/>
                    </Route>
                    <Route path="*" element={<NotFound/>}/>
                </Routes>
            </Router>
        </div>
    );
}

export default App;
