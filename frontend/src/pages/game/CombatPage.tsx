import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import type { Monster } from "../../types/zones";
import type { CombatResult } from "../../types/combat";
import type { Character } from "../../types/characters";

import { getMonster } from "../../api/zones";
import { getMyCharacter } from "../../api/characters";
import { fight } from "../../api/combat";

function CombatPage() {
    const { monsterId, level } = useParams()
    const navigate = useNavigate()
    const [monster, setMonster] = useState<Monster | null>(null)
    const [character, setCharacter] = useState<Character | null>(null)
    const [combatResult, setCombatResult] = useState<CombatResult | null>(null)
    const [levelsGained, setLevelsGained] = useState(0)
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!monsterId || !level) {
            setError("Invalid Monster or Monster Level")
            setIsLoading(false)
            return
        }
        getMonster(monsterId)
        .then(data => setMonster(data))
        .catch(() => {
            setError("Unable to load Monster")
        })
        getMyCharacter()
        .then(data => setCharacter(data))
        .catch(() => {
            setError("Unable to get character info")
        })
        .finally(() => setIsLoading(false))

    }, [monsterId, level])

    const handleFight = async () => {
        setLevelsGained(0)
        setIsLoading(true)
        setError(null)
        // capture level before the fight so we can detect level ups after the result comes back
        const levelBefore = character?.level ?? 0
        fight(monsterId!, parseInt(level!))
        .then(data => {
            setCombatResult(data)
            // re-fetch monster and character to get updated kills, progress, and level
            getMonster(monsterId!)
                .then(m => setMonster(m))
            getMyCharacter()
                .then(c => {
                    if (c.level > levelBefore) setLevelsGained(c.level - levelBefore)
                    setCharacter(c)
            })
        })
        .catch((err) => {
            setError(err.response?.data?.detail || "Couldn't load fight")
        })
        .finally(() => setIsLoading(false))
        
    }

    return (
        <div className="p-6 max-w-5xl mx-auto flex flex-col gap-6">
            {isLoading && <p className="text-parchment">Loading...</p>}
            {error && <p className="text-red-400">{error}</p>}
            {monster && (
                <>
                    <div className="grid grid-cols-3 gap-6">
                        {/* MONSTER STATS */}
                        <div className="bg-surface rounded p-4 border border-bordeaux/30 h-96 overflow-y-auto">
                            <h2 className="text-gold font-bold text-lg">{monster.name}</h2>
                            <p className="text-parchment/60 text-sm mb-3">Level {level}</p>
                            <div className="flex flex-col gap-1 text-parchment text-sm">
                                <span>HP: {monster.base_hp}</span>
                                <span>ATK: {monster.base_attack}</span>
                                <span>DEF: {monster.base_defense}</span>
                                <span className="text-parchment/50 text-xs mt-2">Defeated: {monster.total_kills}x</span>
                            </div>
                        </div>
                        {/* COMBAT LOG */}
                        <div className="bg-surface rounded p-4 border border-bordeaux/30 font-mono text-sm h-96 overflow-y-auto">
                            {combatResult
                            ? combatResult.combat_text.map((line, i) => <p key={i} className="text-parchment">{line}</p>)
                            : <p className="text-parchment/40">Awaiting combat...</p>
                            }
                        </div>
                        {/* PLAYER STATS */}
                        <div className="bg-surface rounded p-4 border border-bordeaux/30 h-96 overflow-y-auto">
                            <h2 className="text-gold font-bold text-lg">{character?.name}</h2>
                            <p className="text-parchment/60 text-sm mb-3">Level {character?.level}</p>
                            <div className="flex flex-col gap-1 text-parchment text-sm">
                                <span>HP: {character?.hp} / {character?.max_hp}</span>
                                <span>ATK: {character?.attack}</span>
                                <span>DEF: {character?.defense}</span>
                                <span>Stamina: {character?.stamina}</span>
                            </div>
                        </div>
                    </div>
                    {/* RESULT BANNER & BUTTONS */}
                    {levelsGained > 0 && (
                        <div className="border border-gold rounded p-3 text-center bg-gold/10 text-gold font-bold text-lg">
                            LEVEL UP! You are now level {character?.level}
                        </div>
                    )}
                    {combatResult && (
                        <div className={`border rounded p-3 text-center font-bold text-xl ${combatResult.winner === "player" 
                        ? "bg-green-900/50 border-green-500 text-green-400" 
                        : "bg-bordeaux/30 border-bordeaux text-red-400"}`}>
                            {combatResult.winner === "player" ? "VICTORY!" : "DEFEAT"}
                            <span className="ml-6 text-gold text-base font-normal">+{combatResult.xp_gained} XP &nbsp; +{combatResult.gold_gained} Gold</span>
                        </div>
                    )}
                    <div className="flex gap-3">
                        <button onClick={handleFight} disabled={isLoading} className="bg-gold text-bg font-bold py-2 px-6 rounded hover:brightness-110 disabled:opacity-50">{combatResult ? "Fight Again" : "Fight"}</button>
                        <button  onClick={() => navigate(`/zones/${monster.zone_id}`)} className="border border-bordeaux/50 text-parchment/70 py-2 px-4 rounded hover:border-bordeaux">Back</button>
                    </div>
                </>
            )}
        </div>
    )
}

export default CombatPage