# This file connects our PostgreSQL database and exposes two endpoints to read adn create users.

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
import datetime

DATABASE_URL = "postgresql://postgres:Valentine@localhost:5433/MentalMath_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(UserCreate):
    user_id: int

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="User Management API")

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()