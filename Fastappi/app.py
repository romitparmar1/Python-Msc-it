from pathlib import Path
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import date

app = FastAPI()

# Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="hello python",
    same_site="lax",
    https_only=False
)

# Database Configuration
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Templates Path Fix
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# Database Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), default=None)
    description = Column(String(300), default=None)
    priority = Column(String(20), default=None)
    is_completed = Column(Boolean, default=False)
    created_by = Column(String(100), nullable=False)
    due_date = Column(Date, default=date.today)


Base.metadata.create_all(bind=engine)

print("Database successfully created")


# Database Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get Logged-in Username
def get_username(request: Request):
    username = request.session.get("username")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Please Login First"
        )

    return username


# Get User Task
def get_user_task(task_id: int, username: str, db: Session):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == username
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return task


# Home Page
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    tasks = db.query(Task).filter(
        Task.created_by == username
    ).order_by(Task.id.desc()).all()

    pending_task = [t for t in tasks if not t.is_completed]
    complited_task = [t for t in tasks if t.is_completed]

    theme = request.cookies.get("theme", "light")

    if theme not in ("light", "dark"):
        theme = "light"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": username,
            "pending_tasks": pending_task,
            "complited_task": complited_task,
            "theme": theme
        }
    )


# Login Page
@app.get("/login")
def login_page(request: Request):
    if request.session.get("username"):
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None}
    )


# Login Function
@app.post("/login")
def login(
    request: Request,
    username: str = Form(...)
):
    username = username.strip()

    if not username or len(username) > 100:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Enter Name Up to 100 Character"
            },
            status_code=400
        )

    request.session.clear()
    request.session["username"] = username

    return RedirectResponse("/", status_code=303)


# Add Task
@app.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    db: Session = Depends(get_db)
):
    username = get_username(request)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(
            status_code=400,
            detail="Title must contain 1 to 150 characters"
        )

    if len(description) > 300:
        raise HTTPException(
            status_code=400,
            detail="Description cannot exceed 300 characters"
        )

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(
            status_code=400,
            detail="Invalid Priority"
        )

    task = Task(
        title=title,
        description=description,
        priority=priority,
        is_completed=False,
        created_by=username,
        due_date=date.today()
    )

    db.add(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# Complete / Incomplete Task
@app.get("/toggle/{id}")
def toggle_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    task.is_completed = not task.is_completed
    db.commit()

    return RedirectResponse("/", status_code=303)


# Edit Task Page
@app.get("/edit/{id}")
def edit_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "task": task,
            "username": username
        }
    )


# Update Task
@app.post("/update/{id}")
def update_task(
    id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150:
        raise HTTPException(
            status_code=400,
            detail="Title must contain 1-150 characters"
        )

    if len(description) > 300:
        raise HTTPException(
            status_code=400,
            detail="Description cannot exceed 300 characters"
        )

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(
            status_code=400,
            detail="Invalid Priority"
        )

    task.title = title
    task.description = description
    task.priority = priority

    db.commit()

    return RedirectResponse("/", status_code=303)


# Delete Task
@app.post("/delete/{id}")
def delete_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_username(request)
    task = get_user_task(id, username, db)

    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# Change Theme
@app.get("/set-theme/{theme}")
def set_theme(
    request: Request,
    theme: str
):
    get_username(request)

    if theme not in ("light", "dark"):
        raise HTTPException(
            status_code=404,
            detail="Theme Must Be Light Or Dark"
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


# Logout
@app.get("/logout")
def logout_task(request: Request):
    request.session.clear()

    return RedirectResponse("/login", status_code=303)
