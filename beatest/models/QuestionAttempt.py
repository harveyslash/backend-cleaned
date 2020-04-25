import enum

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import deferred, relationship

from Sugar import Dictifiable
from extensions import db


class QuestionAttemptStatusEnum(enum.Enum):
    seen = "seen"
    review = "review"
    null = None


class SupportLanguagesEnum(enum.Enum):
    python = "python"
    cpp = "cpp"
    java = "java"


class QuestionAttempt(Dictifiable, db.Model):
    __tablename__ = 'question_attempt'

    section_attempt_id = Column(Integer, ForeignKey('section_attempt.id',
                                                    ondelete="CASCADE"),
                                primary_key=True)
    question_id = Column(Integer,
                         ForeignKey('question.id'),
                         primary_key=True
                         )
    choice_id = Column(Integer, ForeignKey('choice.id'))
    tita_choice = Column(String(50))
    attempt_status = Column(String(50))
    time_spent = Column(Float, nullable=False, default=0)

    chosen_language_id = Column(Integer, ForeignKey("coding_language.id"),
                                nullable=True)

    long_answer = Column(LONGTEXT)

    score = Column(Float(), nullable=True)

    # if attempt was correct
    # will be calculated after test is marked complete
    was_correct = Column(Boolean(), nullable=True)

    # number of correct coding cases
    # will be calculated after test is marked complete
    correct_coding_cases_count = Column(Integer(), nullable=True)
    coding_average_time = Column(Float(), nullable=True)
    coding_max_space = Column(Float(), nullable=True)
    comment_to_code_ratio = Column(Float(), nullable=True)

    section_attempt = relationship('SectionAttempt',
                                   back_populates='question_attempts')

    question = relationship('Question', back_populates='question_attempts')
    choice = relationship('Choice')

    chosen_language = relationship("CodingLanguage")

    def calc_score_on_ques(self, question):
        """
        Calculate the score for a single question

        :param question: Question object.
                         This question must be the same question that
                         this question attempt refers to.

                         In the case of MCQ Questions, this question must have
                         pre-loaded choices with the first element of choices
                         being the correct one (i.e. is_correct = True)


        :return: a tuple indicating the score,didAttempt(boolean),isCorrect(boolean) is returned

        If both tita_choice & choice_id are null , it means the user
                 did not attempt the question. In this case 0,False is returned.

                 If his answer matches the right answer, the value  of
                 points_correct,True is returned

                 If his answer does not match the right answer, the value of
                 -1 * points_wrong,True is returned.
        """
        if self.question_id != question.id:
            raise AttributeError(
                    "QuestionAttempt.question_id does not match Question.id")

        if self.choice_id is None and self.tita_choice is None:
            return 0, False, None

        if self.tita_choice is not None:
            if self.tita_choice == question.tita_answer:
                return question.points_correct, True, True

            if question.points_wrong <= 0:
                return 1 * question.points_wrong, True, False
            else:
                return -1 * question.points_wrong, True, False

        if self.choice_id is not None:

            # means the question has no correct_choice.
            if len(question.choices) < 1:
                return 0, True, True
                # raise Exception("Question attempt has choice id, "
                #                 "but corresponding question has no choices "
                #                 )

            if self.choice_id == question.choices[0].id:
                return question.points_correct, True, True

            if question.points_wrong <= 0:
                return 1 * question.points_wrong, True, False
            else:
                return -1 * question.points_wrong, True, False


        else:
            raise Exception("Case was not handled. We shouldnt be here.")

    @staticmethod
    def can_use_coding_language(language_id, question_id):

        from models import QuestionAllowedLanguages

        if language_id == None:
            return True

        query = (db.session.query(
                QuestionAllowedLanguages.query
                    .filter(
                        QuestionAllowedLanguages.language_id == language_id)
                    .filter(
                        QuestionAllowedLanguages.question_id == question_id)
                    .exists())
                 .scalar())

        return query
