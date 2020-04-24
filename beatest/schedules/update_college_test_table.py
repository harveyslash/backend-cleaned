"""
Update the is_active column for all rows in the test

"""
from datetime import datetime

from extensions import celery, db
from models import CollegeTest


@celery.task()
def update_college_tests():
    now = datetime.now()

    rows = (CollegeTest.query
            .filter(CollegeTest.should_override == False)
            .all())

    for row in rows:
        if row.start_date < now < row.end_date:
            row.is_active = True

        else:
            row.is_active = False

    db.session.commit()
