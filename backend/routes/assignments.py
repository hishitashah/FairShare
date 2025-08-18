from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import ChoreAssignment
from ..schemas import AssignmentCreate, AssignmentUpdate, AssignmentOut

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/", response_model=AssignmentOut)
def create_assignment(payload: AssignmentCreate, db: Session = Depends(get_db)):
    assignment = ChoreAssignment(
        user_id=payload.user_id,
        chore_id=payload.chore_id,
        assigned_date=payload.assigned_date,
        due_date=payload.due_date,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/", response_model=List[AssignmentOut])
def list_assignments(
    user_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(ChoreAssignment)
    if user_id is not None:
        query = query.filter(ChoreAssignment.user_id == user_id)
    return query.all()


@router.get("/{assignment_id}", response_model=AssignmentOut)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(ChoreAssignment).get(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.patch("/{assignment_id}", response_model=AssignmentOut)
def update_assignment(assignment_id: int, payload: AssignmentUpdate, db: Session = Depends(get_db)):
    assignment = db.query(ChoreAssignment).get(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)

    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{assignment_id}", status_code=204)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(ChoreAssignment).get(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return None 