import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Login from'./pages/Login';
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
          <Route path="/" element={<div>Главная страница My_Whip</div>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/dashboard" element={
              <ProtectedRoute>
              <Dashboard />
              </ProtectedRoute>}
          />
      </Routes>
    </Router>
  );
}

export default App;
