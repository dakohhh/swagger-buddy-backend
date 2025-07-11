"""added base_url field to Project Model

Revision ID: 04e253135f6b
Revises: 415f97e06021
Create Date: 2025-05-29 23:22:45.190914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '04e253135f6b'
down_revision: Union[str, None] = '415f97e06021'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('base_url', sqlmodel.sql.sqltypes.AutoString(), server_default="https://example.com/", nullable=True))

    op.alter_column('project', 'base_url', server_default=None, nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'base_url')
    # ### end Alembic commands ###