"""add unique constraint on edges

Revision ID: 772c3f6682b3
Revises: 52f5cdabe30e
Create Date: 2025-08-15 00:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "772c3f6682b3"
down_revision: str | Sequence[str] | None = "52f5cdabe30e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Enforce no duplicate edges for the same roadmap (directed uniqueness)
    op.create_unique_constraint(
        "uq_edges_roadmap_source_target",
        "edges",
        ["roadmap_id", "source_id", "target_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_edges_roadmap_source_target", "edges", type_="unique")
