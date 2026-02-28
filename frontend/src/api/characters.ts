import client from "./client"

export const createCharacter = async (name: string, class_type: string): Promise<void> => {
    await client.post('/characters/', { name, class_type })
}

export const getClassStats = async () => {
    const res = await client.get("/characters/classes")
    return res.data
}

export const getMyCharacter = async () => {
    const res = await client.get('/characters/me')
    return res.data
}