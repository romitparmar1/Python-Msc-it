from fastapi import (
    FastAPI,
    Depends,
    Request,
    Form,
    HTTPException
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from model import Task


# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

app = FastAPI()

# Change this secret before deployment.
app.add_middleware(
    SessionMiddleware,
    secret_key="replace-this-with-a-long-random-secret-key",
    same_site="lax",
    https_only=False
)

templates = Jinja2Templates(directory="templates")

# Automatically create tables when the application starts.
Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# LOGIN REQUIRED
# --------------------------------------------------

def get_logged_in_user(request: Request):
    username = request.session.get("username")

    if not username:
        return None

    return username


# --------------------------------------------------
# HOME: PENDING AND COMPLETED TASKS
# --------------------------------------------------

@app.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_logged_in_user(request)

    if not username:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # Only fetch the logged-in user's tasks.
    tasks = (
        db.query(Task)
        .filter(Task.created_by == username)
        .order_by(Task.created_at.desc())
        .all()
    )

    pending_tasks = [
        task for task in tasks
        if not task.is_completed
    ]

    completed_tasks = [
        task for task in tasks
        if task.is_completed
    ]

    theme = request.cookies.get("theme", "light")

    if theme not in ("light", "dark"):
        theme = "light"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": username,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "theme": theme
        }
    )


# --------------------------------------------------
# GET LOGIN PAGE
# --------------------------------------------------

@app.get("/login")
def login_page(request: Request):
    if get_logged_in_user(request):
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None}
    )


# --------------------------------------------------
# POST LOGIN: SAVE USER IN SESSION
# --------------------------------------------------

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...)
):
    username = username.strip()

    if not username:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Please enter your name."},
            status_code=400
        )

    if len(username) > 100:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Name must be 100 characters or fewer."},
            status_code=400
        )

    # Clear old session data before logging in.
    request.session.clear()
    request.session["username"] = username

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# ADD TASK
# --------------------------------------------------

@app.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = get_logged_in_user(request)

    if not username:
        return RedirectResponse("/login", status_code=303)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(
            status_code=400,
            detail="Title is required and must be at most 150 characters."
        )

    if len(description) > 300:
        raise HTTPException(
            status_code=400,
            detail="Description must be at most 300 characters."
        )

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(
            status_code=400,
            detail="Invalid priority."
        )

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        is_completed=False,
        created_by=username
    )

    db.add(new_task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# TOGGLE TASK COMPLETION
# --------------------------------------------------

@app.get("/toggle/{id}")
def toggle_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_logged_in_user(request)

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    task.is_completed = not task.is_completed
    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# GET EDIT PAGE
# --------------------------------------------------

@app.get("/edit/{id}")
def edit_task_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_logged_in_user(request)

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    theme = request.cookies.get("theme", "light")

    if theme not in ("light", "dark"):
        theme = "light"

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "task": task,
            "username": username,
            "theme": theme
        }
    )


# --------------------------------------------------
# UPDATE TASK
# --------------------------------------------------

@app.post("/update/{id}")
def update_task(
    id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = get_logged_in_user(request)

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(
            status_code=400,
            detail="Title is required and must be at most 150 characters."
        )

    if len(description) > 300:
        raise HTTPException(
            status_code=400,
            detail="Description must be at most 300 characters."
        )

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(
            status_code=400,
            detail="Invalid priority."
        )

    task.title = title
    task.description = description
    task.priority = priority

    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# DELETE TASK
# --------------------------------------------------

@app.post("/delete/{id}")
def delete_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_logged_in_user(request)

    if not username:
        return RedirectResponse("/login", status_code=303)

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# SET THEME COOKIE
# --------------------------------------------------

@app.get("/set-theme/{theme}")
def set_theme(theme: str, request: Request):
    if not get_logged_in_user(request):
        return RedirectResponse("/login", status_code=303)

    if theme not in ("light", "dark"):
        raise HTTPException(
            status_code=400,
            detail="Invalid theme."
        )

    response = RedirectResponse("/", status_code=303)

    response.set_cookie(
        key="theme",
        value=theme,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return response


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse("/login", status_code=303)