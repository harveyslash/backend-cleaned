import csv

from sqlalchemy.orm import contains_eager
from tqdm import tqdm

from extensions import bcrypt
from models import TestAttempt, User, Section


def persist_section_scores_command():
    section = Section.query.join(Section.questions).options(
            contains_eager(Section.questions)).all()[0]
    print(section)
    print(len(section.questions))

    return
    for test_attempt in tqdm(TestAttempt.query.filter(
            TestAttempt.is_complete == True).all()):
        # print(test_attempt.id)
        try:
            TestAttempt.calculate_score_for_test(test_attempt.user_id,
                                                 test_attempt.test_id, True)
        except:
            pass
