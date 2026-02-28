import client from "./client"

export const createCharacter = async (name: string, class_type: string): Promise<void> => {
    await client.post('/characters/', { name, class_type })
}