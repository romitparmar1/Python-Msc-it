from sqlalchemy import Column, String, Integer, Date, DateTime
from database import Base
from datetime import datetime

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    due_date = Column(Date)
    status = Column(String)

    user_id = Column(Integer)
    
class User(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key=True)
    username=Column(String, nullable=False)
    email=Column(String, nullable=False)
    password=Column(String,nullable=False)
    timestamp=Column(DateTime, default=datetime.today, nullable=False)

class LoginTrack(Base):
    __tablename__ = "user_login"
    id=Column(Integer, primary_key=True)
    username=Column(String, nullable=False)
    timestamp=Column(DateTime, default=datetime.today, nullable=False)