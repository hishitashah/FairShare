from datetime import date, timedelta
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models import User, Chore, ChoreAssignment, ChoreLog
from .security import hash_password


def seed():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Clear existing data for repeatable runs (optional)
        db.query(ChoreLog).delete()
        db.query(ChoreAssignment).delete()
        db.query(Chore).delete()
        db.query(User).delete()
        db.commit()

        # Users
        parent = User(
            name="Alex Parent",
            gender="female",
            email="parent@example.com",
            password_hash=hash_password("dev_password"),
            family_relationship="parent",
            created_by=None,
        )
        child = User(
            name="Jamie Kid",
            gender="male",
            email="kid@example.com",
            password_hash=hash_password("dev_password"),
            family_relationship="child",
            created_by=None,
        )
        db.add_all([parent, child])
        db.commit()
        db.refresh(parent)
        db.refresh(child)

        # Chores
        dishes = Chore(name="Do the dishes", category="cleaning", description="Wash and dry dishes")
        vacuum = Chore(name="Vacuum living room", category="cleaning", description="Vacuum all carpets")
        db.add_all([dishes, vacuum])
        db.commit()
        db.refresh(dishes)
        db.refresh(vacuum)

        # Assignments
        assign1 = ChoreAssignment(
            user_id=parent.id,
            chore_id=dishes.id,
            assigned_date=date.today(),
            due_date=date.today() + timedelta(days=1),
        )
        assign2 = ChoreAssignment(
            user_id=child.id,
            chore_id=vacuum.id,
            assigned_date=date.today(),
            due_date=date.today() + timedelta(days=2),
        )
        db.add_all([assign1, assign2])
        db.commit()

        # Logs
        log1 = ChoreLog(
            user_id=parent.id,
            chore_id=dishes.id,
            date_completed=date.today(),
            duration_minutes=25,
            notes="All clean!",
        )
        log2 = ChoreLog(
            user_id=child.id,
            chore_id=vacuum.id,
            date_completed=date.today() - timedelta(days=1),
            duration_minutes=15,
            notes="Quick vacuum",
        )
        db.add_all([log1, log2])
        db.commit()

        print("✅ Seeded users, chores, assignments, and logs.")
        return True
    except Exception as exc:
        db.rollback()
        print(f"❌ Seeding failed: {exc}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    seed() 