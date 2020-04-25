"""add score column for section

Revision ID: 5e3156d011e4
Revises: 133b1038ef0c
Create Date: 2018-12-24 17:40:56.837002+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5e3156d011e4'
down_revision = '133b1038ef0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section_attempt',
                  sa.Column('score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('section_attempt', 'score')
    # ### end Alembic commands ###
