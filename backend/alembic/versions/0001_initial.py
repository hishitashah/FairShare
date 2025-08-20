"""
Initial schema for users, chores, chore_assignments, chore_logs
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("gender", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("relationship", sa.String(length=20), nullable=True),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "chores",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "chore_assignments",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chore_id", sa.Integer(), sa.ForeignKey("chores.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assigned_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
    )
    op.create_index("ix_chore_assignments_user_id", "chore_assignments", ["user_id"], unique=False)
    op.create_index("ix_chore_assignments_chore_id", "chore_assignments", ["chore_id"], unique=False)
    op.create_unique_constraint(
        "uq_chore_assignments_user_chore_date",
        "chore_assignments",
        ["user_id", "chore_id", "assigned_date"],
    )

    op.create_table(
        "chore_logs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chore_id", sa.Integer(), sa.ForeignKey("chores.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date_completed", sa.Date(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_chore_logs_user_id", "chore_logs", ["user_id"], unique=False)
    op.create_index("ix_chore_logs_chore_id", "chore_logs", ["chore_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_chore_logs_chore_id", table_name="chore_logs")
    op.drop_index("ix_chore_logs_user_id", table_name="chore_logs")
    op.drop_table("chore_logs")

    op.drop_constraint("uq_chore_assignments_user_chore_date", "chore_assignments", type_="unique")
    op.drop_index("ix_chore_assignments_chore_id", table_name="chore_assignments")
    op.drop_index("ix_chore_assignments_user_id", table_name="chore_assignments")
    op.drop_table("chore_assignments")

    op.drop_table("chores")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users") 