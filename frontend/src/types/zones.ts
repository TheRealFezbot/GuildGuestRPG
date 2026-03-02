export interface Zone {
    id: string
    name: string
    description: string
    order: number
    recommended_level_min: number
    recommended_level_max: number
    is_unlocked: boolean
}

export interface Monster {
    id: string
    zone_id: string
    name: string
    base_hp: number
    base_attack: number
    base_defense: number
    base_xp_reward: number
    base_gold_min: number
    base_gold_max: number
    order_in_zone: number
    is_zone_boss: boolean
    highest_level_beaten: number
    total_kills: number
    is_unlocked: boolean
    levels: MonsterLevel[]
}

export interface MonsterLevel {
    level: number
    hp_multiplier: number
    attack_multiplier: number
    defense_multiplier: number
    xp_multiplier: number
    gold_multiplier: number
    drop_chance_bonus: number
}