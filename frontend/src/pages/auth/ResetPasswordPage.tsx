import React, { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { resetPassword } from "../../api/auth";
import { useNavigate } from "react-router-dom";

function ResetPasswordPage() {
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [searchParams] = useSearchParams()
    const token = searchParams.get("token")
    const [error, setError] = useState<string | null>(null)
    const navigate = useNavigate()

    const handleSubmit = async (e: React.SyntheticEvent) => {
        e.preventDefault()
        if (!token) {
            return
        }
        if (password !== confirmPassword) {
            setError("Passwords do not match.")
            return
        }
        try {
            await resetPassword(token, password)
            navigate("/login")
        } catch (err: any) {
            const detail = err.response?.data?.detail
            if (typeof detail === "string") {
                setError(detail)
            } else if (Array.isArray(detail) && detail.length > 0) {
                setError(detail[0].msg)
            } else {
                setError("Something went wrong, try again.")
            }
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-bg">
            <div className="bg-surface p-8 rounded-lg w-full max-w-sm flex flex-col gap-4">
                <h1 className="text-gold text-2xl font-bold text-center">Reset Password</h1>
                <p className="text-red-400 text-sm min-h-5">{error ?? ""}</p>
                {!token ? (
                    <p className="text-parchment">Invalid or missing reset link.</p>
                ) : (
                    <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
                        <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full"
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="New password" 
                        />
                        <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full"
                        type="password" 
                        value={confirmPassword} 
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Confirm password" 
                        />
                        <button className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110 w-full" type="submit">Reset Password</button>
                    </form>
                )}
            </div>
        </div>
    )
}

export default ResetPasswordPage