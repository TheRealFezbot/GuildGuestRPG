import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import React from "react";

function ProtectedRoute({ children }: { children: React.ReactNode}) {
    const { user, isLoading } = useAuth()
    if (isLoading) return null
    return user ? <>{children}</> : <Navigate to="/login" />
}

export default ProtectedRoute