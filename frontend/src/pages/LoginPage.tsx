import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";


function LoginPage() {
    const [identifier, setIdentifier] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState<string | null>(null)
    const navigate = useNavigate()
    const { login, user, isLoading } = useAuth()

    const handleSubmit = async (e: React.SyntheticEvent) => {
        e.preventDefault()
        try {
            await login(identifier, password)
            navigate("/")
        } catch {
            setError("Invalid credentials")
        }
    }

    useEffect(() => {
        if (!isLoading && user) {
            navigate("/")
        }
    }, [user, isLoading])

    return (
        <div>
            <h1>Login</h1>
            {error && <p>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input 
                type="text" 
                value={identifier} 
                onChange={(e) => setIdentifier(e.target.value)} 
                placeholder="Username or Email" 
                />
                <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password" 
                />
                <button type="submit">Login</button>
            </form>
        </div>
    )
}

export default LoginPage