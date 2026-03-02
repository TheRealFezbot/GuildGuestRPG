import type { CombatResult } from "../types/combat"
import client from "./client"

export const fight = async (monsterId: string, level: number): Promise<CombatResult> => {
    const res = await client.post("/combat/fight", { monster_id: monsterId, level })
    return res.data
}