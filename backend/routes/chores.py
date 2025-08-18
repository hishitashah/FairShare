from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Chore
from ..schemas import ChoreCreate, ChoreUpdate, ChoreOut

router = APIRouter(prefix="/chores", tags=["chores"])


@router.post("/", response_model=ChoreOut)
def create_chore(payload: ChoreCreate, db: Session = Depends(get_db)):
    chore = Chore(name=payload.name, category=payload.category, description=payload.description)
    db.add(chore)
    db.commit()
    db.refresh(chore)
    return chore


@router.get("/", response_model=List[ChoreOut])
def list_chores(db: Session = Depends(get_db)):
    return db.query(Chore).all()


@router.get("/{chore_id}", response_model=ChoreOut)
def get_chore(chore_id: int, db: Session = Depends(get_db)):
    chore = db.query(Chore).get(chore_id)
    if not chore:
        raise HTTPException(status_code=404, detail="Chore not found")
    return chore


@router.patch("/{chore_id}", response_model=ChoreOut)
def update_chore(chore_id: int, payload: ChoreUpdate, db: Session = Depends(get_db)):
    chore = db.query(Chore).get(chore_id)
    if not chore:
        raise HTTPException(status_code=404, detail="Chore not found")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(chore, field, value)

    db.commit()
    db.refresh(chore)
    return chore


@router.delete("/{chore_id}", status_code=204)
def delete_chore(chore_id: int, db: Session = Depends(get_db)):
    chore = db.query(Chore).get(chore_id)
    if not chore:
        raise HTTPException(status_code=404, detail="Chore not found")
    db.delete(chore)
    db.commit()
    return None 