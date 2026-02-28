import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { verifyEmail } from "../../api/auth";

function VerifyPage() {
    const [isVerified, setIsVerified] = useState<boolean>(false)
    const [searchParams] = useSearchParams()
    const token = searchParams.get("token")
    const [error, setError] = useState<string | null>(null)
    
    useEffect(() => {
        const verify = async () => {
            if (!token) {
                setError("Invalid verification token, try again.")
                return
            }
            try {
                await verifyEmail(token)
                setIsVerified(true)
            } catch {
                setError("Invalid verification token, try again.")
            }
        }
        verify()
    }, [])

    return (
        <div>
            <h1>Email Verification</h1>
            {isVerified && <p>Email verified! <a href="/login">Click here to login</a></p>}
            {error &&<p>{error}</p>}
        </div>
    )
}

export default VerifyPage