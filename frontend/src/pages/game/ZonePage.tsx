import { useParams, useNavigate } from "react-router-dom";
import { getZoneMonsters } from "../../api/zones";
import { useState, useEffect } from "react";
import type { Monster } from "../../types/zones";

function ZonePage() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [selectedLevels, setSelectedLevels] = useState<Record<string, number>>({})
    const [expandedId, setExpandedId] = useState<string | null>(null)
    const [monsters, setMonsters] = useState<Monster[]>([])
    const [error, setError] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        if (!id) {
            setError("Invalid zone")
            setIsLoading(false)
            return
        }
        getZoneMonsters(id)
        .then(data => setMonsters(data))
        .catch(() => {
            setError("Unable to load Zone Monsters")
        })
        .finally(() => setIsLoading(false))
    }, [])

    if (isLoading) return <p className="text-parchment">Loading...</p>
    if (error) return (
        <div>
            <p className="text-red-400">{error}</p>
            <button onClick={() => navigate("/zones")}>← Back</button>
        </div>
    )
    return (
        <div className="flex flex-col gap-3">
            <button onClick={() => navigate("/zones")}>← Back</button>
            {monsters.map(monster => {
                const selectedLevel = selectedLevels[monster.id] ?? 1
                const levelData = monster.levels.find(l => l.level === selectedLevel)
                const powerLevel = Math.round(
                    10 
                    + monster.base_attack * (levelData?.attack_multiplier ?? 1) 
                    + monster.base_defense * (levelData?.defense_multiplier ?? 1) 
                    + Math.floor((monster.base_hp * (levelData?.hp_multiplier ?? 1)) / 2)
                )

                const isExpanded = expandedId === monster.id

            return (
                <div
                    key={monster.id}
                    className={monster.is_unlocked ? "bg-surface border border-gold/20 rounded-lg p-4 cursor-pointer" : "bg-surface border border-gold/20 rounded-lg p-4 opacity-50 cursor-not-allowed"}
                    onClick={monster.is_unlocked ? () => setExpandedId(isExpanded ? null : monster.id) : undefined}
                >
                    <h2>{monster.name}</h2>
                    <p>Power Level: {powerLevel}</p>
                    <p>Progress: {monster.highest_level_beaten}/5</p>
    
                    {isExpanded && (
                        <div className="flex flex-col gap-2" onClick={e => e.stopPropagation()}>
                            <div className="flex gap-3 flex-wrap">
                                {monster.levels.map(level => (
                                    <label 
                                    key={level.level}
                                    className={`bg-bg border rounded-lg px-3 py-1 text-parchment text-sm
                                        ${selectedLevels[monster.id] === level.level ? "border-gold" : "border-gold/30"}
                                        ${level.level > monster.highest_level_beaten + 1 ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
                                    >
                                        <input
                                        className="sr-only"
                                        type="radio"
                                        name={`level-${monster.id}`}
                                        value={level.level}
                                        checked={selectedLevels[monster.id] === level.level}
                                        disabled={level.level > monster.highest_level_beaten + 1}
                                        onChange={() => setSelectedLevels(prev => ({...prev, [monster.id]: level.level}))} />
                                        Level {level.level}
                                    </label>
                                ))}
                            </div>
                            <div>
                                <button className="bg-gold text-bg font-bold py-2 px-4 rounded hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed" disabled={!selectedLevels[monster.id]}>Fight</button>
                            </div>
                        </div>
                    )}
                </div>
            )
        })}
        </div>

    )
}

export default ZonePage
