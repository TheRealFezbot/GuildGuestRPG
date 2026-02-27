import client from "./client"
import type { TokenResponse, User } from "../types/auth"

export const login = async (identifier: string, password: string): Promise<TokenResponse> => {
    const res = await client.post('/auth/login', { email: identifier, username: identifier, password: password })
    return res.data
}

export const register = async (email: string, username: string, password: string, date_of_birth: string): Promise<void> => {
    await client.post('/auth/register', { email, username, password, date_of_birth})
}

export const getMe = async (): Promise<User> => {
    const res = await client.get('/auth/me')
    return res.data
}