import React, { useState } from "react";
import { requestPasswordReset } from "../../api/auth";

function ForgotPasswordPage() {
    const [email, setEmail] = useState("")
    const [message, setMessage] = useState<string | null>(null)

    const handleSubmit = async (e: React.SyntheticEvent) => {
        e.preventDefault()
        await requestPasswordReset(email)
        setMessage("Check your email for a reset link")
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-bg">
            <div className="bg-surface p-8 rounded-lg w-full max-w-sm flex flex-col gap-4">
                <h1 className="text-gold text-2xl font-bold text-center">Request Password Reset</h1>
                <p className="text-parchment text-sm min-h-5">{message ?? ""}</p>
                <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
                    <input className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full"
                    type="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    placeholder="Email" 
                    autoComplete="off"
                    />
                    <button className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110 w-full" type="submit">Request Reset</button>
                </form>
            </div>
        </div>
    )
}

export default ForgotPasswordPage