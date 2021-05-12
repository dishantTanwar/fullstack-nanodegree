"""UPDATE: Show.start_time datatype to str

Revision ID: 83ad4be033cb
Revises: c8e198077ee6
Create Date: 2021-05-12 01:06:57.440757

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '83ad4be033cb'
down_revision = 'c8e198077ee6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'start_time',
               existing_type=sa.String,
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
