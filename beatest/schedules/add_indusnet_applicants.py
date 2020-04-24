"""
Update the is_active column for all rows in the test

"""
from datetime import datetime

from extensions import celery, db
from models import CollegeTest


@celery.task()
def add_indusnet_applicants():
    result = db.engine.execute(
        "insert IGNORE into corporate_applicants (corporate_id, user_id)"
        "SELECT 2,id from user where referral_code_used = 'indusnet2804;'")
