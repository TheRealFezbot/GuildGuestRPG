import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCharacter } from "../api/characters";

function CreateCharacterPage() {
    const [ name, setName ] = useState("")
    const [ selectedClass, setSelectedClass ] = useState<string | null>(null)
    const [ error, setError ] = useState<string | null>(null)
    const navigate = useNavigate()

    const handleSubmit = async (e:React.SyntheticEvent) => {
            e.preventDefault()
            if (!selectedClass) {
                setError("Please select a class.")
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
}