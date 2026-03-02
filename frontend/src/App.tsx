import { BrowserRouter, Routes, Route, Outlet } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

import CreateCharacterPage from "./pages/character/CreateCharacterPage";
import ForgotPasswordPage from "./pages/auth/ForgotPasswordPage";
import ResetPasswordPage from "./pages/auth/ResetPasswordPage";
import RegisterPage from "./pages/auth/RegisterPage";
import VerifyPage from "./pages/auth/VerifyPage";
import ZonesPage from "./pages/game/ZonesPage";
import LoginPage from "./pages/auth/LoginPage";
import ZonePage from "./pages/game/ZonePage";
import HomePage from "./pages/game/HomePage";

import ProtectedRoute from "./components/ProtectedRoute";
import GameLayout from "./components/GameLayout";
import CombatPage from "./pages/game/CombatPage";

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
          <Route element={
            <ProtectedRoute>
              <GameLayout>
                <Outlet />
              </GameLayout>
            </ProtectedRoute>}>
            <Route path="/" element={<HomePage />} />
            <Route path="/character/create" element={<CreateCharacterPage />} />
            <Route path="/zones/" element={<ZonesPage />} />
            <Route path="/zones/:id" element={<ZonePage />} />
            <Route path="/combat/:monsterId/:level" element={<CombatPage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App