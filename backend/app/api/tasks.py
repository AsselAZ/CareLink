from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_senior, require_helper
from app.db.database import get_db
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskCategory
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