"""removeed_all_models_apart_from_users

Revision ID: 778fd40c4476
Revises: ef4c96f895ea
Create Date: 2025-05-11 15:50:37.667978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '778fd40c4476'
down_revision: Union[str, None] = 'ef4c96f895ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###