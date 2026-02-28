import type React from "react";
import NavBar from "./NavBar";

function GameLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-bg flex flex-col">
            <NavBar />
            <main className="flex-1 p-6">
                {children}
            </main>
        </div>
    )
}

export default GameLayout