import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../services/api";


function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await login(email,password)
            console.log("Успешный ответ: ", response)
            localStorage.setItem("token", response.access_token);
            navigate("/dashboard")
        } catch (error) {
            console.log("Ошибка входа: ",error.response?.data || error);
        }
    }
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            <button type="submit">Login</button>
        </form>
    );
}

export default Login;