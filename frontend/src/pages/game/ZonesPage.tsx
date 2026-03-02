import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { Zone } from "../../types/zones";
import { getZones } from "../../api/zones";


function ZonesPage() {
    const navigate = useNavigate()
    const [zones, setZones] = useState<Zone[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        getZones()
        .then(data => setZones(data))
        .catch(() => {
            setError("Unable to load zones")
        })
        .finally(() => setIsLoading(false))
    }, [])

    if (isLoading) return <p className="text-parchment">Loading...</p>
    if (error) return <p className="text-red-400">{error}</p>
    
    return (
        <div className="flex flex-col gap-3">
            {zones.map(zone => (
                <div 
                    key={zone.id}  
                    className={zone.is_unlocked ? "bg-surface border border-gold/20 rounded-lg p-4 cursor-pointer" : "bg-surface border border-gold/20 rounded-lg p-4 opacity-50 cursor-not-allowed"} 
                    onClick={zone.is_unlocked ? () => navigate(`/zones/${zone.id}`) : undefined}
                >
                    <h2 className="text-gold font-bold text-xl">{zone.name}</h2>
                    <p className="text-parchment/70 text-sm mt-1">{zone.description}</p>
                    <p className="text-parchment/50 text-xs mt-2">Levels {zone.recommended_level_min} - {zone.recommended_level_max}</p>
                </div>

            ))}
        </div>
    )
}

export default ZonesPage