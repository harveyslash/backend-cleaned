"""Added sixteen p report table

Revision ID: fc301e1ca8ec
Revises: 02c3ab7ae9a6
Create Date: 2019-05-24 05:40:55.801737+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fc301e1ca8ec'
down_revision = '02c3ab7ae9a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sixteen_p_report',
                    sa.Column('test_attempt_id', sa.Integer(), nullable=False),
                    sa.Column('personality_type', sa.String(length=512),
                              nullable=True),
                    sa.Column('role', sa.String(length=512), nullable=True),
                    sa.Column('strategy', sa.String(length=512),
                              nullable=True),
                    sa.Column('mind_value', sa.Float(), nullable=True),
                    sa.Column('mind_text', sa.Text(), nullable=True),
                    sa.Column('energy_value', sa.Float(), nullable=True),
                    sa.Column('energy_text', sa.Text(), nullable=True),
                    sa.Column('nature_value', sa.Float(), nullable=True),
                    sa.Column('nature_text', sa.Text(), nullable=True),
                    sa.Column('tactics_value', sa.Float(), nullable=True),
                    sa.Column('tactics_text', sa.Text(), nullable=True),
                    sa.Column('identity_value', sa.Float(), nullable=True),
                    sa.Column('identity_text', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['test_attempt_id'],
                                            ['test_attempt.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('test_attempt_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sixteen_p_report')
    # ### end Alembic commands ###
