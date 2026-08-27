from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_senior, require_helper
from app.db.database import get_db
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskCategory, TaskUpdate
from app.models.notification import Notification
from app.services.distance import calculate_distance

from sqlalchemy import select

from app.models.task_details import (
    ShoppingDetails,
    AppointmentDetails,
    FurnitureDetails,
    CraftDetails,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)




@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(require_senior),
    db: Session = Depends(get_db),
):
    # Zuerst wird der allgemeine Task erstellt
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        category=task_data.category.value,
        status=TaskStatus.OPEN.value,
        task_date=task_data.task_date,
        start_time=task_data.start_time,
        end_time=task_data.end_time,
        senior_id=current_user.id,
    )

    db.add(new_task)

    # flush speichert noch nicht endgültig,
    # gibt uns aber schon die neue Task-ID
    db.flush()

    # Je nach Kategorie werden die passenden Zusatzdaten gespeichert
    if task_data.category == TaskCategory.SHOPPING:
        if task_data.shopping_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine Einkaufsanfrage werden Einkaufsdetails benötigt.",
            )

        details = ShoppingDetails(
            task_id=new_task.id,
            shopping_list=task_data.shopping_details.shopping_list,
            store=task_data.shopping_details.store,
        )

        db.add(details)

    elif task_data.category == TaskCategory.APPOINTMENT:
        if task_data.appointment_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine Terminanfrage werden Termindetails benötigt.",
            )

        details = AppointmentDetails(
            task_id=new_task.id,
            location=task_data.appointment_details.location,
            appointment_type=task_data.appointment_details.appointment_type,
        )

        db.add(details)

    elif task_data.category == TaskCategory.FURNITURE:
        if task_data.furniture_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine Möbelanfrage werden Möbeldetails benötigt.",
            )

        details = FurnitureDetails(
            task_id=new_task.id,
            weight_kg=task_data.furniture_details.weight_kg,
            floor=task_data.furniture_details.floor,
            elevator_available=task_data.furniture_details.elevator_available,
        )

        db.add(details)

    elif task_data.category == TaskCategory.CRAFT:
        if task_data.craft_details is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Für eine handwerkliche Anfrage werden zusätzliche Angaben benötigt.",
            )

        details = CraftDetails(
            task_id=new_task.id,
            work_type=task_data.craft_details.work_type,
            required_tools=task_data.craft_details.required_tools,
            difficulty=task_data.craft_details.difficulty,
        )

        db.add(details)

    # Erst jetzt wird Task + Detail gemeinsam dauerhaft gespeichert
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "category": new_task.category,
        "status": new_task.status,
        "senior_id": new_task.senior_id,
    }




# Diese Route ist nur für eingeloggte Helfer zugänglich
@router.post("/{task_id}/accept")
def accept_task(
    task_id: int,
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    # Task anhand seiner ID suchen
    task = db.get(Task, task_id)

    # Prüfen, ob der Task überhaupt existiert
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    # Nur offene Tasks dürfen angenommen werden
    if task.status != TaskStatus.OPEN.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dieser Task ist nicht mehr offen.",
        )

    # Benachrichtigung an den Senior senden
    notification = Notification(
        user_id=task.senior_id,
        message=f"Ein Helfer hat Ihren Task '{task.title}' angenommen.",
    )
    db.add(notification)

    # Eingeloggten Helfer eintragen
    task.helper_id = current_user.id

    # Status ändern
    task.status = TaskStatus.ACCEPTED.value

    db.commit()
    db.refresh(task)

    return task




@router.get("/open")
def get_open_tasks(
    max_distance: float | None = None,
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    open_tasks = db.scalars(
        select(Task).where(Task.status == TaskStatus.OPEN.value)
    ).all()

    result = []

    for task in open_tasks:
        distance_km = None

        if (
            current_user.address
            and current_user.address.latitude is not None
            and current_user.address.longitude is not None
            and task.senior.address
            and task.senior.address.latitude is not None
            and task.senior.address.longitude is not None
        ):
            distance_km = calculate_distance(
                current_user.address.latitude,
                current_user.address.longitude,
                task.senior.address.latitude,
                task.senior.address.longitude,
            )
            # Wenn eine maximale Distanz angegeben ist, prüfen,
            #  ob der Task innerhalb dieser Distanz liegt  
        if (
            max_distance is not None
            and distance_km is not None
            and distance_km > max_distance
        ):
            continue

        result.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "category": task.category,
                "status": task.status,
                "task_date": task.task_date,
                "start_time": task.start_time,
                "end_time": task.end_time,
                "senior_id": task.senior_id,
                "distance_km": distance_km,
            }
        )

    return result




@router.get("/accepted/mine")
def get_my_accepted_tasks(
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    tasks = db.scalars(
        select(Task).where(
            Task.helper_id == current_user.id,
            Task.status == TaskStatus.ACCEPTED.value,
        )
    ).all()

    return tasks



@router.get("/senior/mine")
def get_my_tasks(
    current_user: User = Depends(require_senior),
    db: Session = Depends(get_db),
):
    tasks = db.scalars(
        select(Task).where(
            Task.senior_id == current_user.id
        )
    ).all()

    return tasks




# Diese Route ist nur für eingeloggte Senioren zugänglich
@router.post("/{task_id}/confirm/helper")
def confirm_task_as_helper(
    task_id: int,
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    if task.helper_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dieser Task wurde nicht von Ihnen angenommen.",
        )

    if task.status != TaskStatus.ACCEPTED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nur angenommene Tasks können bestätigt werden.",
        )

    task.helper_confirmed = True

    # Nur wenn der Senior bereits bestätigt hat,
    # ist der Task jetzt wirklich abgeschlossen.
    if task.senior_confirmed:
        task.status = TaskStatus.DONE.value

        senior_notification = Notification(
            user_id=task.senior_id,
            message=f"Der Task '{task.title}' wurde erfolgreich abgeschlossen.",
        )

        helper_notification = Notification(
            user_id=task.helper_id,
            message=f"Der Task '{task.title}' wurde erfolgreich abgeschlossen.",
        )

        db.add(senior_notification)
        db.add(helper_notification)

    db.commit()
    db.refresh(task)

    return task




# Diese Route ist nur für eingeloggte Senioren zugänglich
@router.post("/{task_id}/confirm/senior")
def confirm_task_as_senior(
    task_id: int,
    current_user: User = Depends(require_senior),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    if task.senior_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dieser Task gehört nicht zu Ihnen.",
        )

    if task.status != TaskStatus.ACCEPTED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nur angenommene Tasks können bestätigt werden.",
        )

    task.senior_confirmed = True

    # Wenn der Helfer schon bestätigt hat, ist die Aufgabe abgeschlossen
    if task.helper_confirmed:
        task.status = TaskStatus.DONE.value

        senior_notification = Notification(
            user_id=task.senior_id,
            message=f"Der Task '{task.title}' wurde erfolgreich abgeschlossen.",
        )

        helper_notification = Notification(
            user_id=task.helper_id,
            message=f"Der Task '{task.title}' wurde erfolgreich abgeschlossen.",
        )

        db.add(senior_notification)
        db.add(helper_notification)

    db.commit()
    db.refresh(task)

    return task




@router.get("/helper/done/mine")
def get_my_done_tasks_as_helper(
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    tasks = db.scalars(
        select(Task).where(
            Task.helper_id == current_user.id,
            Task.status == TaskStatus.DONE.value,
        )
    ).all()

    return tasks




@router.get("/senior/done/mine")
def get_my_done_tasks_as_senior(
    current_user: User = Depends(require_senior),
    db: Session = Depends(get_db),
):
    tasks = db.scalars(
        select(Task).where(
            Task.senior_id == current_user.id,
            Task.status == TaskStatus.DONE.value,
        )
    ).all()

    return tasks



@router.post("/{task_id}/cancel")
def cancel_task(
    task_id: int,
    current_user: User = Depends(require_senior),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    if task.senior_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dieser Task gehört nicht zu Ihnen.",
        )

    if task.status == TaskStatus.DONE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ein erledigter Task kann nicht mehr abgebrochen werden.",
        )

    if task.status == TaskStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dieser Task wurde bereits abgebrochen.",
        )

    # Wenn ein Helper beteiligt ist -> Helper informieren/benarichtigen
    if task.helper_id is not None:
        notification = Notification(
            user_id=task.helper_id,
            message=f"Der Senior hat den Task '{task.title}' storniert.",
        )

        db.add(notification)

    task.status = TaskStatus.CANCELLED.value

    db.commit()
    db.refresh(task)

    return task




@router.post("/{task_id}/withdraw")
def withdraw_from_task(
    task_id: int,
    current_user: User = Depends(require_helper),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    # Prüfen: Ist genau dieser Helper dem Task zugeordnet?
    if task.helper_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dieser Task wurde nicht von Ihnen angenommen.",
        )

    # Rückzug nur bei einem angenommenen Task
    if task.status != TaskStatus.ACCEPTED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sie können sich nur von einem angenommenen Task zurückziehen.",
        )

    # Senior informieren
    notification = Notification(
        user_id=task.senior_id,
        message=f"Der Helfer kann den Task '{task.title}' nicht mehr übernehmen. Der Task ist wieder offen.",
    )

    db.add(notification)

    # Helper entfernen und Task wieder freigeben
    task.helper_id = None
    task.helper_confirmed = False
    task.senior_confirmed = False
    task.status = TaskStatus.OPEN.value

    db.commit()
    db.refresh(task)

    return task



@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    # Offene Tasks dürfen Helper sehen.
    # Bei angenommenen/erledigten Tasks dürfen nur die beteiligten Nutzer zugreifen.
    if task.status != TaskStatus.OPEN.value:
        if (
            current_user.id != task.senior_id
            and current_user.id != task.helper_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sie sind nicht an diesem Task beteiligt.",
            )

    details = None

    if task.category == TaskCategory.SHOPPING.value:
        shopping_details = db.scalar(
            select(ShoppingDetails).where(
                ShoppingDetails.task_id == task.id
            )
        )

        if shopping_details:
            details = {
                "shopping_list": shopping_details.shopping_list,
                "store": shopping_details.store,
            }

    elif task.category == TaskCategory.APPOINTMENT.value:
        appointment_details = db.scalar(
            select(AppointmentDetails).where(
                AppointmentDetails.task_id == task.id
            )
        )

        if appointment_details:
            details = {
                "location": appointment_details.location,
                "appointment_type": appointment_details.appointment_type,
            }

    elif task.category == TaskCategory.FURNITURE.value:
        furniture_details = db.scalar(
            select(FurnitureDetails).where(
                FurnitureDetails.task_id == task.id
            )
        )

        if furniture_details:
            details = {
                "weight_kg": furniture_details.weight_kg,
                "floor": furniture_details.floor,
                "elevator_available": furniture_details.elevator_available,
            }

    elif task.category == TaskCategory.CRAFT.value:
        craft_details = db.scalar(
            select(CraftDetails).where(
                CraftDetails.task_id == task.id
            )
        )

        if craft_details:
            details = {
                "work_type": craft_details.work_type,
                "required_tools": craft_details.required_tools,
                "difficulty": craft_details.difficulty,
            }

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "category": task.category,
        "status": task.status,
        "task_date": task.task_date,
        "start_time": task.start_time,
        "end_time": task.end_time,
        "senior_id": task.senior_id,
        "helper_id": task.helper_id,
        "senior_confirmed": task.senior_confirmed,
        "helper_confirmed": task.helper_confirmed,
        "details": details,
    }

# Update a task
@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(require_senior),
    db: Session = Depends(get_db),
):
    # Task anhand der übergebenen ID aus der Datenbank laden
    task = db.get(Task, task_id)

    # Abbrechen, wenn kein Task mit dieser ID existiert
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task wurde nicht gefunden.",
        )

    # Sicherstellen, dass nur der Senior den eigenen Task bearbeiten kann
    if task.senior_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dieser Task gehört nicht zu Ihnen.",
        )

    # Änderungen sind nur möglich, solange noch kein Helper
    # den Task angenommen hat
    if task.status != TaskStatus.OPEN.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nur offene Tasks können bearbeitet werden.",
        )

    # Allgemeine Task-Daten aktualisieren
    # Es werden nur Felder geändert, die tatsächlich
    # vom Nutzer mitgeschickt wurden.

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.task_date is not None:
        task.task_date = task_data.task_date

    if task_data.start_time is not None:
        task.start_time = task_data.start_time

    if task_data.end_time is not None:
        task.end_time = task_data.end_time

    # Kategoriespezifische Daten aktualisieren
    # Je nach Kategorie liegen die Zusatzinformationen
    # in einer eigenen Detailtabelle

    # Einkaufsanfrage
    if (
        task.category == TaskCategory.SHOPPING.value
        and task_data.shopping_details is not None
    ):
        details = db.scalar(
            select(ShoppingDetails).where(
                ShoppingDetails.task_id == task.id
            )
        )

        # Nur übermittelte Einkaufsdetails überschreiben
        if details is not None:
            if task_data.shopping_details.shopping_list is not None:
                details.shopping_list = (
                    task_data.shopping_details.shopping_list
                )

            if task_data.shopping_details.store is not None:
                details.store = task_data.shopping_details.store

    # Terminanfrage
    elif (
        task.category == TaskCategory.APPOINTMENT.value
        and task_data.appointment_details is not None
    ):
        details = db.scalar(
            select(AppointmentDetails).where(
                AppointmentDetails.task_id == task.id
            )
        )

        # Nur übermittelte Termindetails überschreiben
        if details is not None:
            if task_data.appointment_details.location is not None:
                details.location = (
                    task_data.appointment_details.location
                )

            if task_data.appointment_details.appointment_type is not None:
                details.appointment_type = (
                    task_data.appointment_details.appointment_type
                )

    # Möbeltransport
    elif (
        task.category == TaskCategory.FURNITURE.value
        and task_data.furniture_details is not None
    ):
        details = db.scalar(
            select(FurnitureDetails).where(
                FurnitureDetails.task_id == task.id
            )
        )

        # Nur übermittelte Möbeldetails überschreiben
        if details is not None:
            if task_data.furniture_details.weight_kg is not None:
                details.weight_kg = (
                    task_data.furniture_details.weight_kg
                )

            if task_data.furniture_details.floor is not None:
                details.floor = (
                    task_data.furniture_details.floor
                )

            if task_data.furniture_details.elevator_available is not None:
                details.elevator_available = (
                    task_data.furniture_details.elevator_available
                )

    # Handwerkliche Anfrage
    elif (
        task.category == TaskCategory.CRAFT.value
        and task_data.craft_details is not None
    ):
        details = db.scalar(
            select(CraftDetails).where(
                CraftDetails.task_id == task.id
            )
        )

        # Nur übermittelte Handwerksdetails überschreiben
        if details is not None:
            if task_data.craft_details.work_type is not None:
                details.work_type = (
                    task_data.craft_details.work_type
                )

            if task_data.craft_details.required_tools is not None:
                details.required_tools = (
                    task_data.craft_details.required_tools
                )

            if task_data.craft_details.difficulty is not None:
                details.difficulty = (
                    task_data.craft_details.difficulty
                )

    # Alle Änderungen gemeinsam dauerhaft in PostgreSQL speichern
    db.commit()

    # Task erneut aus der Datenbank laden,
    # damit die aktuellen Werte zurückgegeben werden
    db.refresh(task)

    return {
        "message": "Task wurde aktualisiert.",
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "category": task.category,
    }