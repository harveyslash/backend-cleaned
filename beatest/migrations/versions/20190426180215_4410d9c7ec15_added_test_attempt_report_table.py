"""Added test attempt report table

Revision ID: 4410d9c7ec15
Revises: 678c0584f439
Create Date: 2019-04-26 18:02:15.037713+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4410d9c7ec15'
down_revision = '678c0584f439'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_attempt_report',
                    sa.Column('test_attempt_id', sa.Integer(), nullable=False),
                    sa.Column('conceptual_level', sa.Float(), nullable=True),
                    sa.Column('inference_level', sa.Float(), nullable=True),
                    sa.Column('analytical_ability', sa.Float(), nullable=True),
                    sa.Column('mental_math_speed', sa.Float(), nullable=True),
                    sa.Column('data_interpretation_ability', sa.Float(),
                              nullable=True),
                    sa.Column('domain_based_ability', sa.Float(),
                              nullable=True),
                    sa.Column('logical_reasoning_ability', sa.Float(),
                              nullable=True),
                    sa.Column('paragraph_writing_ability', sa.Float(),
                              nullable=True),
                    sa.Column('verbal_ability', sa.Float(), nullable=True),
                    sa.Column('verbal_reasoning', sa.Float(), nullable=True),
                    sa.Column('coding_quality', sa.Float(), nullable=True),
                    sa.Column('is_finished', sa.Boolean(), nullable=False),
                    sa.Column('create_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('last_update_date', sa.DateTime(),
                              nullable=True),
                    sa.Column('finish_date', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['test_attempt_id'],
                                            ['test_attempt.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('test_attempt_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_attempt_report')
    # ### end Alembic commands ###
