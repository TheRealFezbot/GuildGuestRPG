import type { InventoryItem } from "../types/inventory";
import client from "./client";

export const getInventory = async (): Promise<InventoryItem[]> => {
    const res = await client.get("/inventory/")
    return res.data
}

export const equipItem = async (inventoryId: string): Promise<void> => {
    await client.post(`/inventory/${inventoryId}/equip`)
}

export const unequipItem = async (inventoryId: string): Promise<void> => {
    await client.post(`/inventory/${inventoryId}/unequip`)
}