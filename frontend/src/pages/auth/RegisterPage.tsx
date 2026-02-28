import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../../api/auth";
import { useAuth } from "../../context/AuthContext";

function RegisterPage() {
    const [email, setEmail] = useState("")
    const [confirmEmail, setConfirmEmail] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [dateOfBirth, setDateOfBirth] = useState("")
    const [error, setError] = useState<string | null>(null)
    const { user, isLoading } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e:React.SyntheticEvent) => {
        e.preventDefault()
        if (email !== confirmEmail) {
            setError("Emails do not match.")
            return
        }
        if (password !== confirmPassword) {
            setError("Passwords do not match.")
            return
        }
        
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
        <div className="min-h-screen flex items-center justify-center bg-bg">
            <div className="bg-surface p-8 rounded-lg w-full max-w-sm flex flex-col gap-4 min-h-80">
                <h1 className="text-gold text-2xl font-bold text-center">Register</h1>
                <p className="text-red-400 text-sm min-h-5">{error ?? ""}</p>
                <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full" 
                    type="text" 
                    value={username} 
                    onChange={(e) => setUsername(e.target.value)} 
                    placeholder="Username" 
                    />
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full" 
                    type="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    placeholder="Email" 
                    />
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full" 
                    type="email" 
                    value={confirmEmail} 
                    onChange={(e) => setConfirmEmail(e.target.value)} 
                    placeholder="Confirm email" 
                    />
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full" 
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password" 
                    />
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full" 
                    type="password" 
                    value={confirmPassword} 
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm password" 
                    />
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full" 
                    type="date" 
                    value={dateOfBirth} 
                    onChange={(e) => setDateOfBirth(e.target.value)}
                    />
                    <button className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110 w-full" type="submit">Register</button>
                </form>
            </div>
        </div>
    )
}

export default RegisterPage