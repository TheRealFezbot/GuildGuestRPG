import { useState, useEffect } from "react";
import { getInventory, equipItem, unequipItem } from "../../api/inventory";
import type { InventoryItem } from "../../types/inventory";

export default function InventoryPage() {
    const [items, setItems] = useState<InventoryItem[]>([])

    const fetchInventory = async () => {
        const data = await getInventory()
        setItems(data)
    }

    useEffect(() => { fetchInventory() }, [])

    const bag = items.filter(i => i.equipped_slot === null)

    const handleEquip = async (inventoryId: string) => {
        await equipItem(inventoryId)
        fetchInventory()
    }

    const handleUnequip = async (inventoryId: string) => {
        await unequipItem(inventoryId)
        fetchInventory()
    }

    const getSlot = (slot: string) => items.find(i => i.equipped_slot === slot)

    const renderSlot = (slot: string) => {
        const item = getSlot(slot)
        return item ? (
            <div onDoubleClick={() => handleUnequip(item.inventory_id)}
            className="w-24 h-24 bg-surface border border-gold/50 rounded flex flex-col items-center justify-center text-center cursor-pointer hover:border-bordeaux/50 p-2">
                <p className="text-gold text-xs font-bold leading-tight">{item.name}</p>
                <p className="text-parchment/40 text-xs mt-1">{slot}</p>
            </div>
        ) : (
            <div className="w-24 h-24 border border-bordeaux/20 rounded flex items-center justify-center text-parchment/20 text-xs capitalize">
                {slot}
            </div>
        )
    }

    return (
        <div className="flex gap-16 w-full max-w-4xl mx-auto items-start">
            {/* Equipment Panel */}
            <div>
                <h2 className="text-gold text-lg font-bold mb-4">Equipment</h2>
                <div className="grid grid-cols-3 gap-3" style={{ gridTemplateRows: 'repeat(3, 6rem)' }}>
                    <div className="col-start-2 row-start-1">{renderSlot('head')}</div>
                    <div className="col-start-3 row-start-1">{renderSlot('accessory')}</div>
                    <div className="col-start-1 row-start-2">{renderSlot('weapon')}</div>
                    <div className="col-start-2 row-start-2">{renderSlot('chest')}</div>
                    <div className="col-start-3 row-start-2">{renderSlot('offhand')}</div>
                    <div className="col-start-2 row-start-3">{renderSlot('legs')}</div>
                </div>
            </div>

            {/* Bag */}
            <div className="flex-1 max-w-2xl">
                <h2 className="text-gold text-lg font-bold mb-4">Bag</h2>
                <div className="flex flex-wrap gap-3">
                {bag.map(item => (
                    <div key={item.inventory_id} onDoubleClick={() => handleEquip(item.inventory_id)}
                    className="w-32 h-32 bg-surface border border-bordeaux/30 rounded flex flex-col items-center justify-center text-center cursor-pointer hover:border-gold/50 p-3">
                        <p className="text-gold text-sm font-bold leading-tight">{item.name}</p>
                        <p className="text-parchment/50 text-xs mt-1 capitalize">{item.type}</p>
                        <p className="text-parchment/30 text-xs capitalize">{item.rarity}</p>
                    </div>
                ))}
                </div>
            </div>
        </div>
    )
}