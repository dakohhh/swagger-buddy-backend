"""added body  header pathparameters and  queryparameter

Revision ID: cc929b2fd02a
Revises: e91cc1a6f504
Create Date: 2025-05-31 05:53:27.380259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cc929b2fd02a'
down_revision: Union[str, None] = 'e91cc1a6f504'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('body',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('endpoint_id', sa.Uuid(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('descriptive_value', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('required', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoint.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('header',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('endpoint_id', sa.Uuid(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('descriptive_value', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('required', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoint.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pathparameter',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('endpoint_id', sa.Uuid(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('descriptive_value', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('required', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoint.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('queryparameter',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('endpoint_id', sa.Uuid(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('descriptive_value', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('required', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoint.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('endpoint', 'query_parameters')
    op.drop_column('endpoint', 'body')
    op.drop_column('endpoint', 'path_parameters')
    op.drop_column('endpoint', 'headers')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('endpoint', sa.Column('headers', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('endpoint', sa.Column('path_parameters', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('endpoint', sa.Column('body', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('endpoint', sa.Column('query_parameters', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_table('queryparameter')
    op.drop_table('pathparameter')
    op.drop_table('header')
    op.drop_table('body')
    # ### end Alembic commands ###