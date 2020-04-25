""" Add id column to college_test table

Revision ID: 2c45f28c1fd5
Revises: 5c7067e03a07
Create Date: 2018-11-21 17:54:51.717800+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2c45f28c1fd5'
down_revision = '5c7067e03a07'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "ALTER TABLE college_test ADD CONSTRAINT college_test_unique_1 UNIQUE (college_id, test_id);")
    op.execute(
        "ALTER TABLE college_test drop primary key, ADD COLUMN id INTEGER UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT; ")
    op.execute("alter table college_test change college_id college_id int")


def downgrade():
    print("Downgrade is not supported")
