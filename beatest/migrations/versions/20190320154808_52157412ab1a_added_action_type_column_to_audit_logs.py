"""added action type column to audit logs

Revision ID: 52157412ab1a
Revises: 0069697d62b3
Create Date: 2019-03-20 15:48:08.119068+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '52157412ab1a'
down_revision = '0069697d62b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('audit_log', sa.Column('action_type', sa.String(length=500),
                                         nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('audit_log', 'action_type')
    # ### end Alembic commands ###
