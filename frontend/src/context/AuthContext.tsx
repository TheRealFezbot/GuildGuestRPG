import React, { createContext, useContext, useState, useEffect } from "react";
import type { User } from "../types/auth";
import { login as loginApi, getMe } from "../api/auth"

interface AuthContextType {
    user: User | null
    isLoading: boolean
    login: (identifier: string, password: string) => Promise<void>
    logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null)
    const [isLoading, setIsLoading] = useState(true)
    
    useEffect(() => {
        const restore = async () => {
            const token = localStorage.getItem("access_token")
            if (token) {
                try {
                    const userData = await getMe()
                    setUser(userData)
                } catch {
                    localStorage.removeItem("access_token")
                    localStorage.removeItem("refresh_token")
                }
            }
            setIsLoading(false)
        }
        restore()
}, [])

    const login = async (identifier: string, password: string) => {
        const tokens = await loginApi(identifier, password)
        localStorage.setItem("access_token", tokens.access_token)
        localStorage.setItem("refresh_token", tokens.refresh_token)
        const userData = await getMe()
        setUser(userData)
    }

    const logout = () => {
        localStorage.removeItem("access_token")
        localStorage.removeItem("refresh_token")
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, isLoading, login, logout}}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const ctx = useContext(AuthContext)
    if (!ctx) throw new Error("useAuth must be used inside AuthProvider")
    return ctx
}