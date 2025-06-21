import {BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom";
import Login from './pages/Login';
import Me from "./pages/Profile.jsx";
import ProfileEdit from "./pages/ProfileEdit.jsx";
import ProtectedRoute from "./components/ProtectedRoute";
import Signup from "./pages/Signup";
import Home from "./pages/Home.jsx";
import AppLayout from "./pages/AppLayout.jsx";
import CarsList from "./pages/CarList.jsx";
import CarCard from "./components/CarCard.jsx";
import Profile from "./pages/Profile.jsx";

function App() {
    return (
        <div className="App">
            <Router>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/signup" element={<Signup/>}/>

                    <Route path="/app" element={<ProtectedRoute><AppLayout/></ProtectedRoute>}>
                        <Route index element={<Navigate to="cars"/>}/>
                        <Route path="cars" element={<CarsList/>}/>
                        <Route path="cars/:id" element={<CarCard/>}/>
                        <Route path="profile" element={<Profile/>}/>
                        <Route path="profile/edit" element={<ProfileEdit/>}/>
                    </Route>
                </Routes>
            </Router>
        </div>
    );
}

export default App;
