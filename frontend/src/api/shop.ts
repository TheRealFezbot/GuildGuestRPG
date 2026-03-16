import type { BuyResponse, ShopResponse } from "../types/shop";
import client from "./client";

export const getShopItems = async (zoneId: string): Promise<ShopResponse[]> => {
    const res = await client.get(`/shop/${zoneId}`)
    return res.data
}


export const buyItem = async (zoneId: string, itemId: string): Promise<BuyResponse> => {
    const res = await client.post(`/shop/${zoneId}/buy/${itemId}`)

    return res.data
}
