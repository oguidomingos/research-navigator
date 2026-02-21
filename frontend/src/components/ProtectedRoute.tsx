import { useAuth } from "@clerk/clerk-react";
import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isLoaded, userId } = useAuth();

  // Aguardar carregamento
  if (!isLoaded) {
    return (
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh"
      }}>
        <p>Carregando...</p>
      </div>
    );
  }

  // Redirecionar para login se não autenticado
  if (!userId) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
