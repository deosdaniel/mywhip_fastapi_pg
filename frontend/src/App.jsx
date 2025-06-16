import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Login from'./pages/Login';
import Me from "./pages/Me.jsx";
import EditProfile from "./pages/EditProfile.jsx";
import ProtectedRoute from "./components/ProtectedRoute";
import Signup from "./pages/Signup";
function App() {
  return (
      <div className="App">
      <Router>
      <Routes>
          <Route path="/" element={<div>Главная страница My_Whip</div>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<Signup/>} />
          <Route path="/me" element={<ProtectedRoute><Me /></ProtectedRoute>}/>
          <Route path="/me/edit" element={<ProtectedRoute><EditProfile /></ProtectedRoute>}/>

      </Routes>
      </Router>
      </div>
  );
}

export default App;
