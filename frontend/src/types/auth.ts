export interface TokenResponse {
    access_token: string
    refresh_token: string
}

export interface User {
    id: string
    email: string
    username: string
    is_verified: boolean
    is_admin: boolean
    is_banned: boolean
}