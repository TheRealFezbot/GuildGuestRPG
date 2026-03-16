export interface ShopResponse {
    listing_id: string
    id: string
    name: string
    type: string
    rarity: string
    class_type: string | null
    attack_bonus: number
    defense_bonus: number
    hp_bonus: number
    buy_price: number
    sell_price: number
    level_requirement: number
    stock: number | null
}

export interface BuyResponse {
    message: string
    item_name: string
    gold_remaining: number
}
