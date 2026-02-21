"""
Clerk JWT Authentication for FastAPI

Middleware para validar tokens JWT do Clerk.
"""

from typing import Optional
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
import os

# Security scheme
security = HTTPBearer()

# Clerk JWKS URL (onde ficam as chaves públicas para validar JWT)
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API_URL", "")

# Cliente para buscar chaves públicas
if CLERK_JWKS_URL:
    jwks_client = PyJWKClient(CLERK_JWKS_URL)
else:
    jwks_client = None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Valida o token JWT do Clerk e retorna os dados do usuário.

    Args:
        credentials: Credenciais HTTP Bearer (token JWT)

    Returns:
        dict: Dados do usuário extraídos do token

    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    token = credentials.credentials

    if not jwks_client:
        raise HTTPException(
            status_code=500,
            detail="Clerk authentication not configured. Set CLERK_JWKS_URL environment variable."
        )

    try:
        # Obter a chave pública do Clerk
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Validar e decodificar o token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=CLERK_FRONTEND_API,
            options={"verify_exp": True}
        )

        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "email_verified": payload.get("email_verified"),
            "name": payload.get("name"),
            "metadata": payload.get("public_metadata", {}),
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Authentication error: {str(e)}"
        )


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security, auto_error=False)
) -> Optional[dict]:
    """
    Versão opcional do get_current_user.
    Retorna None se não houver token ao invés de lançar exceção.

    Útil para endpoints que podem funcionar com ou sem autenticação.
    """
    if not credentials:
        return None

    try:
        return get_current_user(credentials)
    except HTTPException:
        return None


# Exemplo de uso em um endpoint:
"""
from fastapi import APIRouter, Depends
from app.core.clerk_auth import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello {user['email']}!",
        "user_id": user["user_id"]
    }

@router.get("/optional")
async def optional_route(user: dict | None = Depends(get_current_user_optional)):
    if user:
        return {"message": f"Hello {user['email']}!"}
    else:
        return {"message": "Hello anonymous!"}
"""
