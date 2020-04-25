"""Converted points_correct and points_wrong to float

Revision ID: 532b956bd90f
Revises: 772b0c803712
Create Date: 2017-08-14 23:30:14.712183

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '532b956bd90f'
down_revision = '772b0c803712'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'points_correct',
                    existing_type=mysql.FLOAT(display_width=11),
                    nullable=False, default=0)
    op.alter_column('question', 'points_wrong',
                    existing_type=mysql.FLOAT(display_width=11),
                    nullable=False, default=0)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'points_wrong',
                    existing_type=mysql.INTEGER(display_width=11))
    op.alter_column('question', 'points_correct',
                    existing_type=mysql.INTEGER(display_width=11))
    # ### end Alembic commands ###
