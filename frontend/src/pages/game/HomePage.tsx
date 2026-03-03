import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import type { Character } from "../../types/characters"
import { getMyCharacter } from "../../api/characters"
import type { Zone } from "../../types/zones"
import { getZones } from "../../api/zones"

function HomePage() {
    const navigate = useNavigate()
    const [character, setCharacter] = useState<Character | null>(null)
    const [isLoading, setIsLoading] = useState(true)
    const [displayStamina, setDisplayStamina] = useState<number | null>(0)
    const [zones, setZones] = useState<Zone[]>([])

    useEffect(() => {
        getMyCharacter()
        .then(data => {
            setCharacter(data)
            setDisplayStamina(data.stamina)
        }) 
        .catch(err => {
            if (err.response?.status === 404) {
                navigate("/character/create")
            }
        getZones()
        .then(data => setZones(data))
        })
        .finally(() => setIsLoading(false))
    }, [])

    useEffect(() => {
        if (!character) return
        const interval = setInterval(() => {
            const updatedAt = new Date(character.stamina_updated_at)
            const minutesSince = (Date.now() - updatedAt.getTime()) / 60000
            const regen = Math.floor(minutesSince / 3)
            setDisplayStamina(Math.min(100, character.stamina + regen))
        }, 60000)
        return () => clearInterval(interval)
    }, [character])
    
    if (isLoading) return <p className="text-parchment">Loading...</p>
    if (!character) return null

    return (
        <div className="flex flex-col gap-6">
            {/* CHARACTER HEADER */}
            <div className="bg-surface border border-gold/20 rounded-lg p-6 flex items-center justify-between">
                <div>
                    <h1 className="text-gold text-2xl font-bold">{character.name}</h1>
                    <p className="text-parchment/70 text-sm capitalize">{character.class_type} · Level {character.level}</p>
                </div>
                <div className="text-right">
                    <p className="text-parchment/50 text-xs uppercase tracking-wide">Power Level</p>
                    <p className="text-gold font-bold text-xl">{character.power_level}</p>
                </div>
            </div>

            {/* MAIN GRID */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                {/* STATS */}
                <div className="bg-surface border border-gold/20 rounded-lg p-4 flex flex-col gap-3">
                    <h2 className="text-gold font-bold">Stats</h2>
                    <div>
                        <div className="flex justify-between text-sm text-parchment/70 mb-1">
                            <span>HP</span>
                            <span>{character.hp} / {character.max_hp}</span>
                        </div>
                        <div className="bg-bg rounded-full h-2">
                            <div className="bg-red-500 h-2 rounded-full" style={{ width: `${(character.hp / character.max_hp) * 100}%` }} />
                        </div>
                    </div>
                    <div className="flex justify-between text-parchment text-sm">
                        <span>Stamina</span>
                        <span className="font-bold">{displayStamina}</span>
                    </div>
                    <div className="flex justify-between text-parchment text-sm">
                        <span>Attack</span>
                        <span className="font-bold">{character.attack}</span>
                    </div>
                    <div className="flex justify-between text-parchment text-sm">
                        <span>Defense</span>
                        <span className="font-bold">{character.defense}</span>
                    </div>
                </div>

                {/* EQUIPMENT */}
                <div className="bg-surface border border-gold/20 rounded-lg p-4 flex flex-col gap-3">
                    <h2 className="text-gold font-bold">Equipment</h2>
                    <div className="grid grid-cols-2 gap-2">
                        {["Head", "Chest", "Legs", "Weapon", "Offhand", "Accessory"].map(slot => (
                            <div key={slot} className="bg-bg border border-gold/10 rounded p-2 text-center">
                                <p className="text-parchment/40 text-xs">{slot}</p>
                                <p className="text-parchment/20 text-xs">Empty</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* ZONE PROGRESS */}
                <div className="bg-surface border border-gold/20 rounded-lg p-4 flex flex-col gap-3">
                    <h2 className="text-gold font-bold">Zone Progress</h2>
                    {zones.map(zone => (
                        <div key={zone.id} className="flex justify-between text-sm">
                            <span className="text-parchment">{zone.name}</span>
                            <span className={zone.is_unlocked ? "text-green-400" : "text-parchment/30"}>
                            {zone.is_unlocked ? "Unlocked" : "Locked"}
                            </span>
                        </div>
                        ))}
                </div>

            </div>

            {/* BOTTOM GRID */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                {/* GOLD & XP */}
                <div className="bg-surface border border-gold/20 rounded-lg p-4 flex flex-col gap-3">
                    <h2 className="text-gold font-bold">Wealth</h2>
                    <div className="flex justify-between text-parchment text-sm">
                        <span>Gold</span>
                        <span className="font-bold text-gold">{character.gold}</span>
                    </div>
                    <div className="flex justify-between text-parchment text-sm">
                        <span>XP</span>
                        <span className="font-bold">{character.xp} / {Math.round(100 * Math.pow(character.level, 1.5))}</span>
                    </div>
                    <div className="bg-bg rounded-full h-2">
                        <div className="bg-emerald-700 h-2 rounded-full" style={{ width: `${(character.xp / Math.round(100 * Math.pow(character.level, 1.5))) * 100}%` }} />
                    </div>
                </div>

                {/* PVP */}
                <div className="bg-surface border border-gold/20 rounded-lg p-4 flex flex-col gap-3">
                    <h2 className="text-gold font-bold">PvP</h2>
                    <p className="text-parchment/30 text-sm">— Coming soon —</p>
                </div>

                {/* GUILD */}
                <div className="bg-surface border border-gold/20 rounded-lg p-4 flex flex-col gap-3">
                    <h2 className="text-gold font-bold">Guild</h2>
                    <p className="text-parchment/30 text-sm">— Coming soon —</p>
                </div>

            </div>
        </div>
    )
}

export default HomePage