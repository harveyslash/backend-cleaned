"""empty message

Revision ID: 2e108b010781
Revises: 24574c03b675
Create Date: 2019-01-17 15:02:55.535488+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2e108b010781'
down_revision = '24574c03b675'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('question_ibfk_1', 'question', type_='foreignkey')
    op.drop_column('question', 'section_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question',
                  sa.Column('section_id', mysql.INTEGER(display_width=11),
                            autoincrement=False, nullable=True))
    op.create_foreign_key('question_ibfk_1', 'question', 'section',
                          ['section_id'], ['id'])
    # ### end Alembic commands ###
