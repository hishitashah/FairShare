from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


# User Schemas
class UserBase(BaseModel):
    name: str
    gender: str
    email: EmailStr
    family_relationship: Optional[str] = None
    created_by: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    family_relationship: Optional[str] = None
    created_by: Optional[int] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    gender: str
    email: EmailStr
    family_relationship: Optional[str] = None
    created_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# Chore Schemas
class ChoreBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None


class ChoreCreate(ChoreBase):
    pass


class ChoreUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


class ChoreOut(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Assignment Schemas
class AssignmentBase(BaseModel):
    user_id: int
    chore_id: int
    assigned_date: date
    due_date: Optional[date] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    user_id: Optional[int] = None
    chore_id: Optional[int] = None
    assigned_date: Optional[date] = None
    due_date: Optional[date] = None


class AssignmentOut(BaseModel):
    id: int
    user_id: int
    chore_id: int
    assigned_date: date
    due_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


# Log Schemas
class LogBase(BaseModel):
    user_id: int
    chore_id: int
    date_completed: date
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None


class LogCreate(LogBase):
    pass


class LogUpdate(BaseModel):
    user_id: Optional[int] = None
    chore_id: Optional[int] = None
    date_completed: Optional[date] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None


class LogOut(BaseModel):
    id: int
    user_id: int
    chore_id: int
    date_completed: date
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 