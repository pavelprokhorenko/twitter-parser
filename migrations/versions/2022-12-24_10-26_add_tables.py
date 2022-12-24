"""add tables

Revision ID: 7cc6e7935208
Revises:
Create Date: 2022-12-24 10:26:48.310697+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7cc6e7935208"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "parsing_session",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("twitter_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=127), nullable=True),
        sa.Column("username", sa.String(length=15), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("following_count", sa.Integer(), nullable=True),
        sa.Column("followers_count", sa.Integer(), nullable=True),
        sa.Column(
            "parse_status",
            sa.Enum("FAILED", "PENDING", "SUCCESS", name="parse_user_statuses"),
            server_default="PENDING",
            nullable=False,
        ),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["parsing_session.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username", "session_id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
    op.drop_table("parsing_session")
    # ### end Alembic commands ###