export interface InventoryItem {
    inventory_id: string
    id: string
    name: string
    type: string
    rarity: string
    class_type: string
    attack_bonus: number
    defense_bonus: number
    hp_bonus: number
    buy_price: number
    sell_price: number
    level_requirement: number
    equipped_slot: string | null
}