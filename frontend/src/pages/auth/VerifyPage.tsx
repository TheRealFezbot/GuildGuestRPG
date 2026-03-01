import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { verifyEmail } from "../../api/auth";
import { Link } from "react-router-dom";

function VerifyPage() {
    const [isVerified, setIsVerified] = useState<boolean>(false)
    const [isLoading, setIsLoading] = useState(true)
    const [searchParams] = useSearchParams()
    const token = searchParams.get("token")
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const verify = async () => {
            if (!token) {
                setError("Invalid verification token, try again.")
                setIsLoading(false)
                return
            }
            try {
                await verifyEmail(token)
                setIsVerified(true)
            } catch {
                setError("Invalid verification token, try again.")
            } finally {
                setIsLoading(false)
            }
        }
        verify()
    }, [])

    return (
        <div className="min-h-screen flex items-center justify-center bg-bg">
            <div className="bg-surface p-8 rounded-lg w-full max-w-sm flex flex-col gap-4 text-center min-h-48">
                <h1 className="text-gold text-2xl font-bold">Email Verification</h1>
                {isLoading && <p className="text-parchment/70">Verifying your email...</p>}
                {isVerified && (
                    <>
                        <p className="text-parchment">Your email has been verified!</p>
                        <Link to="/login" className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110">
                            Continue to Login
                        </Link>
                    </>
                )}
                {error && <p className="text-red-400 text-sm">{error}</p>}
            </div>
        </div>
    )
}

export default VerifyPage
