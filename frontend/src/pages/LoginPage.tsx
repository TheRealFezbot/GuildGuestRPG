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
        <div className="min-h-screen flex items-center justify-center bg-bg">
            <div className="bg-surface p-8 rounded-lg w-full max-w-sm flex flex-col gap-4 min-h-80">
                <h1 className="text-gold text-2xl font-bold text-center">Login</h1>
                <p className="text-red-400 text-sm min-h-5">{error ?? ""}</p>
                <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full"
                    type="text" 
                    value={identifier} 
                    onChange={(e) => setIdentifier(e.target.value)} 
                    placeholder="Username or Email" 
                    autoComplete="off"
                    />
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full"
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password" 
                    autoComplete="current-password"
                    />
                    <button className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110 w-full" type="submit">Login</button>
                </form>
            </div>
        </div>
    )
}

export default LoginPage