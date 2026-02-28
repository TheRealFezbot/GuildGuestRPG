import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useState } from "react";

function NavBar() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()
    const [menuOpen, setMenuOpen] = useState(false)
    
    const handleLogout = async () => {
            logout()
            navigate("/login")
        }
    
    return (
        <nav className="bg-surface border-b border-gold/20">
            <div className="px-6 py-3 flex items-center justify-between">
                {/* TITLE */}
                <span className="text-gold font-bold text-lg">Guild Guest RPG</span>

                {/* NAV LINKS — desktop */}
                <div className="hidden md:flex gap-6 text-sm">
                    <Link to="/" className="text-parchment hover:text-gold">Dashboard</Link>
                    <span className="text-parchment/30 cursor-not-allowed">Zones</span>
                    <span className="text-parchment/30 cursor-not-allowed">Shop</span>
                    <span className="text-parchment/30 cursor-not-allowed">Inventory</span>
                    <span className="text-parchment/30 cursor-not-allowed">PvP</span>
                    <span className="text-parchment/30 cursor-not-allowed">Guild</span>
                </div>

                {/* USERNAME/LOGOUT (HAMBURGER) */}
                <div className="flex items-center gap-4">
                    <span className="text-parchment/70 text-sm capitalize">{user?.username}</span>
                    <button onClick={handleLogout} className="text-sm text-parchment hover:text-gold">Logout</button>
                    {/* HAMBURGER - mobile */}
                    <button onClick={() => setMenuOpen(prev => !prev)} className="md:hidden text-parchment hover:text-gold text-xl">
                        {menuOpen ? "✕" : "☰"}
                    </button>
                </div>
            </div>

            {/* MOBILE DROPDOWN */}
            {menuOpen && (
                <div className="md:hidden flex flex-col px-6 pb-4 gap-3 text-sm border-t border-gold/10">
                    <Link to="/" className="text-parchment hover:text-gold" onClick={() => setMenuOpen(false)}>Dashboard</Link>
                    <span className="text-parchment/30 cursor-not-allowed">Zones</span>
                    <span className="text-parchment/30 cursor-not-allowed">Shop</span>
                    <span className="text-parchment/30 cursor-not-allowed">Inventory</span>
                    <span className="text-parchment/30 cursor-not-allowed">PvP</span>
                    <span className="text-parchment/30 cursor-not-allowed">Guild</span>
                </div>
            )}
        </nav>
    )
}

export default NavBar