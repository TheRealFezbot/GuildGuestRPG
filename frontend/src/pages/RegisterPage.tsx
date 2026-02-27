import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth";
import { useAuth } from "../context/AuthContext";

function RegisterPage() {
    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [dateOfBirth, setDateOfBirth] = useState("")
    const [error, setError] = useState<string | null>(null)
    const { user, isLoading } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e:React.SyntheticEvent) => {
        e.preventDefault()
        try {
            await register(email, username, password, dateOfBirth)
            navigate("/login")
        } catch (err: any) {
            const detail = err.response?.data?.detail
            if (typeof detail === "string") {
                setError(detail)
            } else if (Array.isArray(detail) && detail.length > 0) {
                setError(detail[0].msg)
            } else {
                setError("Registration failed")
            }
        }
    }

    useEffect(() => {
            if (!isLoading && user) {
                navigate("/")
            }
        }, [user, isLoading])

    return (
        <div>
            <h1>Register</h1>
            {error && <p>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                placeholder="Email" 
                />
                <input 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                placeholder="Username" 
                />
                <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password" 
                />
                <input 
                type="date" 
                value={dateOfBirth} 
                onChange={(e) => setDateOfBirth(e.target.value)}
                />
                <button type="submit">Register</button>
            </form>
        </div>
    )
}

export default RegisterPage