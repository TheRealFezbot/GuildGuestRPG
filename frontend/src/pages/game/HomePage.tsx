import { useAuth } from "../../context/AuthContext"
import { useNavigate } from "react-router-dom"

function HomePage() {
    const { logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = async () => {
            logout()
            navigate("/login")
        }
    
    return (
        <div className="min-h-screen flex items-center justify-center bg-bg">
            <div className="bg-surface p-8 rounded-lg flex flex-col gap-4">
                <h1 className="text-gold text-2xl font-bold text-center">HOMEPAGE</h1>
                <button className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110" onClick={handleLogout}>Logout</button>
                <button className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110" onClick={() => navigate("/character/create")}>Create Character</button>

            </div>
        </div>
    )
}

export default HomePage