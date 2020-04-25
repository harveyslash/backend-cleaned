"""empty message

Revision ID: 0c93057970e3
Revises: 6a6386eec41f
Create Date: 2019-10-03 18:50:17.479156+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c93057970e3'
down_revision = '6a6386eec41f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_attempt_report', sa.Column('attention_to_detail', sa.Float(), nullable=True))
    op.add_column('test_attempt_report', sa.Column('creative_thinking', sa.Float(), nullable=True))
    op.add_column('test_attempt_report', sa.Column('integrity_quotient', sa.Float(), nullable=True))
    op.add_column('test_attempt_report', sa.Column('people_management', sa.Float(), nullable=True))
    op.add_column('test_attempt_report', sa.Column('strategy_and_decision', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_attempt_report', 'strategy_and_decision')
    op.drop_column('test_attempt_report', 'people_management')
    op.drop_column('test_attempt_report', 'integrity_quotient')
    op.drop_column('test_attempt_report', 'creative_thinking')
    op.drop_column('test_attempt_report', 'attention_to_detail')
    # ### end Alembic commands ###
