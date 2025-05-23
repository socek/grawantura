"""Add is_deleted for questions

Revision ID: 05f461ac6ae7
Revises: 94c06ec1c2c6
Create Date: 2025-03-31 17:59:34.071712

"""

from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "05f461ac6ae7"
down_revision: Union[str, None] = "94c06ec1c2c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("questions", sa.Column("is_deleted", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("questions", "is_deleted")
    # ### end Alembic commands ###
