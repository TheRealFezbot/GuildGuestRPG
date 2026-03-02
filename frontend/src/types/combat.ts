export interface CombatResult {
    winner: string
    xp_gained: number
    gold_gained: number
    item_dropped_id: string | null
    turns_taken: number
    damage_dealt: number
    damage_taken: number
    combat_text: string[]
}