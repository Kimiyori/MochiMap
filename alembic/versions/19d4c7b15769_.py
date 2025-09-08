"""Add ON DELETE CASCADE to node/edge foreign key relationships.

Revision ID: 19d4c7b15769
Revises: 772c3f6682b3
Create Date: 2025-09-06 20:15:07.296795
"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "19d4c7b15769"
down_revision: str | Sequence[str] | None = "772c3f6682b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing foreign key constraints and recreate them with ON DELETE CASCADE.
    # Note: Default Postgres constraint names use the pattern <table>_<column>_fkey.
    # Adjust names below if your DB uses different constraint names.

    # edges -> roadmaps
    op.drop_constraint('edges_roadmap_id_fkey', 'edges', type_='foreignkey')
    op.create_foreign_key(
        'edges_roadmap_id_fkey',
        source_table='edges',
        referent_table='roadmaps',
        local_cols=['roadmap_id'],
        remote_cols=['id'],
        ondelete='CASCADE',
    )

    # edges -> nodes (source)
    op.drop_constraint('edges_source_id_fkey', 'edges', type_='foreignkey')
    op.create_foreign_key(
        'edges_source_id_fkey',
        source_table='edges',
        referent_table='nodes',
        local_cols=['source_id'],
        remote_cols=['id'],
        ondelete='CASCADE',
    )

    # edges -> nodes (target)
    op.drop_constraint('edges_target_id_fkey', 'edges', type_='foreignkey')
    op.create_foreign_key(
        'edges_target_id_fkey',
        source_table='edges',
        referent_table='nodes',
        local_cols=['target_id'],
        remote_cols=['id'],
        ondelete='CASCADE',
    )

    # nodes -> roadmaps
    op.drop_constraint('nodes_roadmap_id_fkey', 'nodes', type_='foreignkey')
    op.create_foreign_key(
        'nodes_roadmap_id_fkey',
        source_table='nodes',
        referent_table='roadmaps',
        local_cols=['roadmap_id'],
        remote_cols=['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate the original foreign keys without ON DELETE CASCADE.

    # edges -> roadmaps
    op.drop_constraint('edges_roadmap_id_fkey', 'edges', type_='foreignkey')
    op.create_foreign_key(
        'edges_roadmap_id_fkey',
        source_table='edges',
        referent_table='roadmaps',
        local_cols=['roadmap_id'],
        remote_cols=['id'],
    )

    # edges -> nodes (source)
    op.drop_constraint('edges_source_id_fkey', 'edges', type_='foreignkey')
    op.create_foreign_key(
        'edges_source_id_fkey',
        source_table='edges',
        referent_table='nodes',
        local_cols=['source_id'],
        remote_cols=['id'],
    )

    # edges -> nodes (target)
    op.drop_constraint('edges_target_id_fkey', 'edges', type_='foreignkey')
    op.create_foreign_key(
        'edges_target_id_fkey',
        source_table='edges',
        referent_table='nodes',
        local_cols=['target_id'],
        remote_cols=['id'],
    )

    # nodes -> roadmaps
    op.drop_constraint('nodes_roadmap_id_fkey', 'nodes', type_='foreignkey')
    op.create_foreign_key(
        'nodes_roadmap_id_fkey',
        source_table='nodes',
        referent_table='roadmaps',
        local_cols=['roadmap_id'],
        remote_cols=['id'],
    )
