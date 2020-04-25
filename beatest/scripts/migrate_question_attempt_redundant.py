import csv

from sqlalchemy.orm import contains_eager, load_only
from tqdm import tqdm

from extensions import bcrypt
from models import TestAttempt, User, Section


def migrate_question_attempt_was_correct_command():
    """
    Calculate and persist the 'was_correct" field
    """

    for test_attempt in tqdm(TestAttempt.query.options(
            load_only(TestAttempt.test_id, TestAttempt.user_id)).all()):

        try:
            TestAttempt.calculate_score_for_test(test_attempt.user_id,
                                                 test_attempt.test_id, True)
        except Exception as e:
            tqdm.write(str(e))
            pass

    return
