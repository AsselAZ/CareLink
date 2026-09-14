from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.database import get_db
from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserCreate, UserProfileUpdate
from app.services.geocoding import geocode_address
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
        birth_date=user_data.birth_date,
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
        "birth_date": new_user.birth_date,
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

# Eigenes Profil anzeigen
@router.get("/me/profile")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    # Prüfen, ob der Nutzer eine Adresse besitzt
    if current_user.address is None:
        address = None
    else:
        address = {
            "street": current_user.address.street,
            "house_number": current_user.address.house_number,
            "postal_code": current_user.address.postal_code,
            "city": current_user.address.city,
            "latitude": current_user.address.latitude,
            "longitude": current_user.address.longitude,
        }

    return {
        "user_id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role,
        "address": address,
    }


# Eigenes Profil bearbeiten
@router.put("/me/profile")
def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Vorname nur ändern, wenn er mitgeschickt wurde
    if profile_data.first_name is not None:
        current_user.first_name = profile_data.first_name

    # Nachname nur ändern, wenn er mitgeschickt wurde
    if profile_data.last_name is not None:
        current_user.last_name = profile_data.last_name

    # Adresse nur ändern, wenn eine Adresse mitgeschickt wurde
    if profile_data.address is not None:

        # Adresse über Nominatim in GPS-Koordinaten umwandeln
        coordinates = geocode_address(
            profile_data.address.street,
            profile_data.address.house_number,
            profile_data.address.postal_code,
            profile_data.address.city,
        )

        latitude = None
        longitude = None

        # Falls Nominatim die Adresse gefunden hat
        if coordinates is not None:
            latitude, longitude = coordinates

        # Nutzer besitzt bereits eine Adresse
        if current_user.address:
            current_user.address.street = profile_data.address.street
            current_user.address.house_number = profile_data.address.house_number
            current_user.address.postal_code = profile_data.address.postal_code
            current_user.address.city = profile_data.address.city
            current_user.address.latitude = latitude
            current_user.address.longitude = longitude

        # Nutzer besitzt noch keine Adresse
        else:
            new_address = Address(
                street=profile_data.address.street,
                house_number=profile_data.address.house_number,
                postal_code=profile_data.address.postal_code,
                city=profile_data.address.city,
                latitude=latitude,
                longitude=longitude,
                user_id=current_user.id,
            )

            db.add(new_address)

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profil wurde aktualisiert.",
        "user_id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role,
    }