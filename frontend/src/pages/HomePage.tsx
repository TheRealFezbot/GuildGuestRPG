import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

function HomePage() {
    const { logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = async () => {
            logout()
            navigate("/login")
        }
    
    return (
        <div>
            <h1>HOMEPAGE</h1>
            <button onClick={handleLogout}>Logout</button>
        </div>
    )
}

export default HomePage