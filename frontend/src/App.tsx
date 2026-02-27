import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<div>Login page</div>} />
          <Route path="/register" element={<div>Register page</div>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App