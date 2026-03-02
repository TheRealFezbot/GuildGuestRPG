import client from "./client"

export const getZones = async () => {
    const res = await client.get("/zones/")
    return res.data
}

export const getZoneMonsters = async (zoneId: string) => {
    const res = await client.get(`/zones/${zoneId}/monsters`)
    return res.data
}

export const getMonster = async (monsterId: string) => {
    const res = await client.get(`/zones/monsters/${monsterId}`)
    return res.data
}