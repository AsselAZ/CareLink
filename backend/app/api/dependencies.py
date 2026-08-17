from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User


#Liest den Bearertoken aus dem Authorization headerr
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        user_id = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ist ungültig oder abgelaufen.",
        )

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nutzer wurde nicht gefunden.",
        )

    return user

# Diese Funktion erlaubt nur eingeloggte Senioren
def require_senior(
    current_user: User = Depends(get_current_user),
):
    # Diese Funktion erlaubt nur eingeloggte Senioren
    if current_user.role != "senior":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Diese Funktion ist nur für Senioren verfügbar.",
        )

    return current_user

# Diese Funktion erlaubt nur eingeloggte Helfer
def require_helper(
    current_user: User = Depends(get_current_user),
):
    # Diese Funktion erlaubt nur eingeloggte Helfer
    if current_user.role != "helper":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Diese Funktion ist nur für Helfer verfügbar.",
        )

    return current_user