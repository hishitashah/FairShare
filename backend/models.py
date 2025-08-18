from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    # Use Python attribute name different from column name to avoid masking sqlalchemy.orm.relationship
    family_relationship = Column("relationship", String(20))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Self-referential relationships
    creator = relationship("User", remote_side=[id], back_populates="created_members")
    created_members = relationship("User", back_populates="creator", foreign_keys=[created_by])

    # Relations to chores
    assignments = relationship("ChoreAssignment", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("ChoreLog", back_populates="user", cascade="all, delete-orphan")


class Chore(Base):
    __tablename__ = "chores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)

    assignments = relationship("ChoreAssignment", back_populates="chore", cascade="all, delete-orphan")
    logs = relationship("ChoreLog", back_populates="chore", cascade="all, delete-orphan")


class ChoreAssignment(Base):
    __tablename__ = "chore_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    chore_id = Column(Integer, ForeignKey("chores.id", ondelete="CASCADE"))
    assigned_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="assignments")
    chore = relationship("Chore", back_populates="assignments")


class ChoreLog(Base):
    __tablename__ = "chore_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    chore_id = Column(Integer, ForeignKey("chores.id", ondelete="CASCADE"))
    date_completed = Column(Date, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="logs")
    chore = relationship("Chore", back_populates="logs") 