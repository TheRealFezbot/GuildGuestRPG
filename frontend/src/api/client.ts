import axios from 'axios'
import { refresh } from './auth'

const client = axios.create({
    baseURL: '/api',
})

client.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

client.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401 && !error.config?.url?.startsWith('/auth/')) {
            try {
                // Check for refresh token, if refresh token refresh the access token
                const refreshToken = localStorage.getItem('refresh_token')
                if (!refreshToken) throw new Error()
                const tokens = await refresh(refreshToken)
                localStorage.setItem('access_token', tokens.access_token)
                localStorage.setItem('refresh_token', tokens.refresh_token)
                return client(error.config)
            } catch {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                window.location.href = '/login'
            }
        }
        return Promise.reject(error)
    }
)

export default client