from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from model import Todo as TodoModel, User, LoginTrack

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os 

# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# JWT CONFIG
# --------------------------------------------------

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --------------------------------------------------
# CREATE JWT TOKEN
# --------------------------------------------------

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# --------------------------------------------------
# DATABASE TABLE CREATE
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# PYDANTIC MODELS
# --------------------------------------------------

class Todo(BaseModel):
    name: str
    due_date: date
    status: str


class UserSignup(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def read_root():
    return {
        "Hello": "Python"
    }


# --------------------------------------------------
# SIGNUP
# --------------------------------------------------

@app.post("/signup")
def signup_todo(
    us: UserSignup,
    db: Session = Depends(get_db)
):

    # Check username already exists
    user = db.query(User).filter(
        User.username == us.username
    ).first()

    if user is not None:
        raise HTTPException(
            status_code=400,
            detail="User Already Exists"
        )

    # Create new user
    newUser = User(
        username=us.username,
        email=us.email,
        password=us.password
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return {
        "message": "User Created Successfully",
        "user": newUser.username
    }


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.post("/login")
def todo_login(
    ul: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user
    l_user = db.query(User).filter(
        User.username == ul.username,
        User.password == ul.password
    ).first()

    # User not found
    if l_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )

    # Generate JWT token
    token = create_access_token(
        data={
            "sub": l_user.username
        }
    )

    # Login tracking
    userLog = LoginTrack(
        username=l_user.username
    )

    db.add(userLog)
    db.commit()
    db.refresh(userLog)

    return {
        "message": "User Login Successfully",
        "access_token": token,
        "token_type": "bearer"
    }


# --------------------------------------------------
# GET CURRENT USER FROM JWT
# --------------------------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token"
    )

    try:

        # Decode token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get username from token
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Find user from database
    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise credentials_exception

    return user


# --------------------------------------------------
# ITEMS
# --------------------------------------------------

@app.get("/items/{item_id}")
def get_item_id(
    item_id: int,
    user_id: int
):

    return {
        "Item_id": item_id,
        "User_Id": user_id
    }


# --------------------------------------------------
# ADD TODO
# JWT REQUIRED
# --------------------------------------------------

@app.post("/adds/")
def create_task(
    task: Todo,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:

        newTask = TodoModel(
            name=task.name,
            due_date=task.due_date,
            status=task.status,

            # IMPORTANT
            # Todo belongs to logged-in user
            user_id=current_user.id
        )

        db.add(newTask)
        db.commit()
        db.refresh(newTask)

        return {
            "details": "Data Saved Successfully",
            "todo_id": newTask.id,
            "user": current_user.username
        }

    except Exception as e:

        db.rollback()

        return {
            "error": "Something went wrong",
            "details": str(e)
        }


# --------------------------------------------------
# GET TODOS
# JWT REQUIRED
# --------------------------------------------------

@app.get("/get/")
def show_todo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only logged-in user's todos
    todos = db.query(TodoModel).filter(
        TodoModel.user_id == current_user.id
    ).all()

    return todos


# --------------------------------------------------
# UPDATE TODO
# JWT REQUIRED
# --------------------------------------------------

@app.put("/update/{edit_id}")
def edit_data(
    edit_id: int,
    task: Todo,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find todo belonging to current user
    todos = db.query(TodoModel).filter(
        TodoModel.id == edit_id,
        TodoModel.user_id == current_user.id
    ).first()

    if todos is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Update
    todos.name = task.name
    todos.due_date = task.due_date
    todos.status = task.status

    db.commit()
    db.refresh(todos)

    return {
        "details": "Record Updated Successfully",
        "data": todos
    }


# --------------------------------------------------
# DELETE TODO
# JWT REQUIRED
# --------------------------------------------------

@app.delete("/delete/{delete_id}")
def delete_todo(
    delete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find todo belonging to current user
    todos = db.query(TodoModel).filter(
        TodoModel.id == delete_id,
        TodoModel.user_id == current_user.id
    ).first()

    if todos is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db.delete(todos)
    db.commit()

    return {
        "details": "Record Deleted Successfully",
        "data": {
            "id": delete_id
        }
    }