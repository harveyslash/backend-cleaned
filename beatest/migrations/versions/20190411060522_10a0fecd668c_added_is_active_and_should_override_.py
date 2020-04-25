"""Added is_active and should_override columns to college_test

Revision ID: 10a0fecd668c
Revises: 52157412ab1a
Create Date: 2019-04-11 06:05:22.114552+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '10a0fecd668c'
down_revision = '52157412ab1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('college_test',
                  sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('college_test',
                  sa.Column('should_override', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('college_test', 'should_override')
    op.drop_column('college_test', 'is_active')
    # ### end Alembic commands ###
