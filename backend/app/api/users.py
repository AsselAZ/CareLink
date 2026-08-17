from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.api.dependencies import (
    get_current_user,
    require_helper,
    require_senior,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    # Prüfen, ob die E-Mail bereits verwendet wird
    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Diese E-Mail-Adresse wird bereits verwendet.",
        )

    # Passwort wird vor dem Speichern gehasht
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role.value,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "role": new_user.role,
    }

@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    #Gibt die Daten des aktuell eingeloggten Nutzers zurück
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role,
    }
# Diese Route ist nur für eingeloggte Senioren zugänglich
@router.get("/senior-test")
def senior_test(
    current_user: User = Depends(require_senior),
):
    return {
        "message": "Senior-Bereich erlaubt",
        "user_id": current_user.id,
    }

# Diese Route ist nur für eingeloggte Helfer zugänglich
@router.get("/helper-test")
def helper_test(
    current_user: User = Depends(require_helper),
):
    return {
        "message": "Helfer-Bereich erlaubt",
        "user_id": current_user.id,
    }