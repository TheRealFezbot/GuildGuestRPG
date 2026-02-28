import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import VerifyPage from "./pages/auth/VerifyPage";
import ProtectedRoute from "./components/ProtectedRoute";
import HomePage from "./pages/game/HomePage";
import CreateCharacterPage from "./pages/character/CreateCharacterPage";
import ForgotPasswordPage from "./pages/auth/ForgotPasswordPage";
import ResetPasswordPage from "./pages/auth/ResetPasswordPage";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/auth/verify" element={<VerifyPage />} />
          <Route path="/auth/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/auth/reset-password" element={<ResetPasswordPage />} />
          <Route path="/character/create" element={<ProtectedRoute><CreateCharacterPage /></ProtectedRoute>} />
          <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App