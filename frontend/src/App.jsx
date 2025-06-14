import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Login from'./pages/Login';
import Dashboard from "./pages/Dashboard.jsx";
//import ProtectedRoute from "./components/ProtectedRoute";
import Signup from "./pages/Signup";
function App() {
  return (
      <div className="App">
    <Router>
      <Routes>
          <Route path="/" element={<div>Главная страница My_Whip</div>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<Signup/>} />
          <Route path="/dashboard" element={
             // <ProtectedRoute>
              <Dashboard />
              //</ProtectedRoute>
          }
          />
      </Routes>
    </Router>
      </div>
  );
}

export default App;
