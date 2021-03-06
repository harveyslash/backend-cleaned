"""added spelling penalty column

Revision ID: ddae49b79e7b
Revises: 0abbb42a0ea2
Create Date: 2019-02-17 17:00:23.681306+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ddae49b79e7b'
down_revision = '0abbb42a0ea2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question',
                  sa.Column('spelling_penalty', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'spelling_penalty')
    # ### end Alembic commands ###
