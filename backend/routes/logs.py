from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import ChoreLog
from ..schemas import LogCreate, LogUpdate, LogOut

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/", response_model=LogOut)
def create_log(payload: LogCreate, db: Session = Depends(get_db)):
    log = ChoreLog(
        user_id=payload.user_id,
        chore_id=payload.chore_id,
        date_completed=payload.date_completed,
        duration_minutes=payload.duration_minutes,
        notes=payload.notes,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/", response_model=List[LogOut])
def list_logs(
    user_id: Optional[int] = Query(default=None),
    chore_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(ChoreLog)
    if user_id is not None:
        query = query.filter(ChoreLog.user_id == user_id)
    if chore_id is not None:
        query = query.filter(ChoreLog.chore_id == chore_id)
    return query.all()


@router.get("/{log_id}", response_model=LogOut)
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ChoreLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log


@router.patch("/{log_id}", response_model=LogOut)
def update_log(log_id: int, payload: LogUpdate, db: Session = Depends(get_db)):
    log = db.query(ChoreLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(log, field, value)

    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=204)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ChoreLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return None 