import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCharacter, getClassStats, getMyCharacter } from "../../api/characters";

function CreateCharacterPage() {
    const [ name, setName ] = useState("")
    const [ selectedClass, setSelectedClass ] = useState<string | null>(null)
    const [ error, setError ] = useState<string | null>(null)
    const navigate = useNavigate()
    const [classStats, setClassStats] = useState<Record<string, { hp: number; attack: number; defense: number }> | null>(null)

    useEffect(() => {
        getMyCharacter()
        .then(() => navigate("/"))
        .catch(() => {})

        getClassStats().then(data => setClassStats(data))
    }, [])

    const handleSubmit = async (e:React.SyntheticEvent) => {
            e.preventDefault()
            if (!selectedClass) {
                setError("Please select a class.")
                return
            }
            if (!name.trim()) {
                setError("Please enter a character name.")
                return
            }
            try {
                await createCharacter(name, selectedClass)
                navigate("/")
            } catch (err: any) {
                const detail = err.response?.data?.detail
                if (typeof detail === "string") {
                    setError(detail)
                } else if (Array.isArray(detail) && detail.length > 0) {
                    setError(detail[0].msg)
                } else {
                    setError("Couldn't create character, try again.")
                }
            }
        }
    
        return (
            <div className="flex justify-center">
                <div className="bg-surface p-8 rounded-lg w-full max-w-3xl flex flex-col gap-6">
                    <h1 className="text-gold text-2xl font-bold text-center">Create Your Character</h1>
                    <form onSubmit={handleSubmit} className="flex flex-col gap-8 w-full max-w-3xl">
                        <div className="flex gap-8">
                            {/* STATS PANEL */}
                            <div className="w-48 shrink-0 bg-surface rounded-lg p-4 text-parchment flex flex-col gap-2">
                                {selectedClass && classStats ? (
                                    <>
                                        <p>HP: {classStats[selectedClass].hp}</p>
                                        <p>Attack: {classStats[selectedClass].attack}</p>
                                        <p>Defense: {classStats[selectedClass].defense}</p>
                                    </>
                                ) : (
                                    <p>Select a class to preview stats</p>
                                )}
                            </div>
                            {/* CHARACTER CLASS PANEL*/}
                            <div className="grid grid-cols-2 gap-4 flex-1">
                                {["warrior", "mage", "rogue", "ranger"].map(cls => (
                                    <label key={cls} htmlFor={cls} className={`cursor-pointer bg-bg border rounded-lg p-4 
                                    ${selectedClass === cls ? "border-gold" : "border-gold/30"}`}>
                                        <input type="radio" id={cls} name="class_type" value={cls} className="sr-only" onChange={() => setSelectedClass(cls)} />
                                        <p className="capitalize font-semibold">{cls}</p>
                                    </label>
                                ))}
                            </div>
                        </div>
                        {/* CHARACTER NAME INPUT */}
                        <input type="text" placeholder="Character name" value={name} onChange={e => setName(e.target.value)} 
                        className="bg-bg text-parchment border border-gold/30 rounded px-3 py-2 w-full" />
                        <p className="text-red-400 text-sm min-h-5">{error ?? ""}</p>
                        <button type="submit" className="bg-gold text-bg font-bold py-2 rounded hover:brightness-110 w-full">
                            Create Character
                        </button>
                    </form>
                </div>
            </div>
        )
}

export default CreateCharacterPage