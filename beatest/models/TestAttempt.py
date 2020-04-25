import random
from datetime import datetime
from difflib import ndiff

import numpy as np
from flask_login import current_user
from scipy import stats
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, \
    Sequence, and_
from sqlalchemy.orm import contains_eager, load_only, relationship
from sqlalchemy.orm.exc import NoResultFound

import Externals
import re
from Sugar import Dictifiable
from extensions import celery, db
from models import SixteenPReport


def compute_partial_match_score(user_output, correct_output):
    """
    Compute a line by line match using diffs.
    testing


    :param user_output: the output that the user produced
    :param correct_output: the expected output
    :return:
    """

    if user_output == None:
        user_output = ""

    if correct_output == None:
        user_output = ""

    user_output = user_output.splitlines(True)

    correct_output = correct_output.splitlines(True)

    diff_count = 0

    for diff in ndiff(correct_output, user_output):
        if diff[0] == '-':
            return 0

        if diff[0] == "+" or diff[0] == "-":
            diff_count += 1

    if diff_count > len(correct_output):
        return 0

    mismatch_score_percentage = diff_count / len(correct_output)

    return 1 - mismatch_score_percentage


class TestAttempt(Dictifiable, db.Model):
    __tablename__ = 'test_attempt'

    id = Column(Integer, Sequence('test_attempt_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    test_id = Column(Integer, ForeignKey('test.id'))
    is_complete = Column(Boolean)
    date = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer, nullable=True)

    is_graded = Column(Boolean, default=False, nullable=False)
    focus_lost_count = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="test_attempts")
    test = relationship("Test", back_populates="test_attempts")
    section_attempts = relationship("SectionAttempt",
                                    back_populates='test_attempt',
                                    cascade="all, delete-orphan")

    report = relationship("TestAttemptReport",
                          back_populates="test_attempt",
                          uselist=False)

    sixteen_p_report = relationship("SixteenPReport",
                                    back_populates="test_attempt",
                                    uselist=False)

    @staticmethod
    def can_user_view_solutions(user_id: int, test_id: int):
        """
        Check to see if user can view solutions to a particular Test.
        A user can view solutions if :
            * There exist at least one Test Attempt
            * No test attempt has is_complete = False

        :return: True if user can view sections, False if not.
        """
        from models import TestAttempt
        test_attempts = (TestAttempt
                         .query
                         .options(load_only(TestAttempt.is_complete))
                         .distinct(TestAttempt.is_complete)
                         .filter(TestAttempt.user_id == user_id)
                         .filter(TestAttempt.test_id == test_id)
                         .all())

        for test_attempt in test_attempts:
            if test_attempt.is_complete == False:
                return False

        return True

    @staticmethod
    def setup_test_attempt(test_id, user_id):
        """
        Create testattempt,sectionattempt and questionattempt for a user.

        **Note** this will not do any access checking.

        :param test_id:
        :param user_id:
        :return: the section id of the first section.
                This is used to set the
                current section in the pinger cookie
        """
        from models import (Section, SectionAttempt, QuestionAttempt,
                            QuestionSection, Question)

        attempt = TestAttempt(
                user_id=user_id,
                test_id=test_id,
                is_complete=False,
        )

        sections = (Section.query
                    .filter(Section.test_id == test_id)
                    .options(load_only(Section.id))
                    .order_by(Section.id.asc())
                    .all()
                    )

        section_attempts = [
            SectionAttempt(section_id=section.id, is_complete=False,
                           time_spent=0) for section
            in sections]

        first_section_id = min(section_attempts,
                               key=lambda x: x.section_id).section_id

        section_attempts = {section_attempt.section_id: section_attempt for
            section_attempt in section_attempts}

        # get all the questions that are part of the test , through
        # sections(and through QuestionSection)
        questions = (Question.query
                     .join(QuestionSection,
                           Question.id == QuestionSection.question_id)
                     .join(Section,
                           and_(QuestionSection.section_id == Section.id,
                                QuestionSection.section_id.in_(
                                        section.id for section in sections)))
                     .options(
                contains_eager(Question.sections).load_only(Section.id))
                     .options(load_only(Question.id))
                     .order_by(QuestionSection.section_id.asc())
                     .all()
                     )

        questions = {question.id: question for question in questions}

        question_attempts = [
            QuestionAttempt(question_id=question.id) for question in
            questions.values()
        ]

        db.session.add(attempt)

        # create section attempts for the newly created test attempt
        for section_attempt in section_attempts.values():
            attempt.section_attempts.append(section_attempt)

            # create question attempts for the newly created section attempt
            for question_attempt in question_attempts:
                question_id = question_attempt.question_id
                question = questions[question_id]
                section = question.sections[0]

                if section.id == section_attempt.section_id:
                    section_attempt.question_attempts.append(question_attempt)

        db.session.commit()

        return first_section_id

    @staticmethod
    def get_percentile_for_score(score, test_id):
        from models import CollegeTest, User
        """
        :param score:
        :param test_id:
        :return:
        """

        test_attempts_query = (TestAttempt.query
                               .options(load_only(TestAttempt.score))
                               .filter(TestAttempt.is_complete != False)
                               .filter(TestAttempt.score != None)
                               .filter(TestAttempt.test_id == test_id)
                               )

        if current_user is not None and current_user.college_id is not None:
            college_test_query = (CollegeTest.query.filter(
                    CollegeTest.college_id == current_user.college_id)
                                  .filter(CollegeTest.test_id == test_id)
                                  )

            # the test belongs to the college that the user is in

            if db.session.query(college_test_query.exists()).scalar():
                users = (User.query
                         .options(load_only(User.id))
                         .filter(User.college_id == current_user.college_id)
                         )
                user_ids = [user.id for user in users]

                test_attempts_query = (test_attempts_query.filter(
                        TestAttempt.user_id.in_(user_ids)
                ))

        test_attempts = test_attempts_query.all()

        arr = [test_attempt.score for test_attempt in test_attempts]
        arr = np.array(arr)
        arr.sort()

        percentile = stats.percentileofscore(arr, score)

        rank = arr[::-1].tolist().index(score) + 1

        output = {
            'percentile': int(percentile.round(decimals=2)),
            'rank': rank,
            'median': float(np.median(arr)),
            'max': float(np.max(arr)),
            'min': float(np.min(arr))
        }
        return output

    @staticmethod
    def calculate_score_for_test(user_id, test_id, should_persist):
        """

        :param user_id:
        :param test_id:
        :param should_persist:
        :return:
        """
        from models import (Test, Section, Choice, Question, SectionAttempt,
                            QuestionAttempt, Error, CodingCase,
                            TestAttemptReport)

        try:
            test = (Test.query
                    .outerjoin(Test.sections)  # can be avoided
                    .outerjoin(Section.questions)  # can be avoided
                    .outerjoin(Choice, and_(Choice.is_correct == True,
                                            Choice.question_id == Question.id))
                    .outerjoin(CodingCase)
                    .join(TestAttempt,
                          and_(TestAttempt.test_id == test_id,
                               TestAttempt.user_id ==
                               user_id))

                    .outerjoin(SectionAttempt)
                    .outerjoin(QuestionAttempt)
                    .options(
                    contains_eager(Test.sections).load_only(Section.id)
                        .contains_eager(Section.questions)
                        .contains_eager(Question.choices))
                    .options(contains_eager(Test.sections).contains_eager(
                    Section.questions).contains_eager(Question.coding_cases))

                    .options(contains_eager(Test.test_attempts)
                             .load_only(TestAttempt.id)
                             .contains_eager(TestAttempt.section_attempts)
                             .contains_eager(SectionAttempt.question_attempts)
                             )

                    .options(load_only(Test.id))
                    .filter(TestAttempt.user_id == user_id)
                    .filter(Test.id == test_id)
                    .one())

            # a dict with key = question id , and value = question itself
            question_bank = {q.id: q for section in test.sections for q in
                section.questions}

            # print(question_bank)

            gradable_question_count = 0
            for question in question_bank.values():
                # print(question.type)
                if question.type == "CODING" or question.type == "SUBJECTIVE":
                    gradable_question_count += 1

            # a list of all the question attempts across all the sections of the test
            all_question_attempts = [attempt for section_attempt in
                test.test_attempts[0].section_attempts for attempt in
                section_attempt.question_attempts]

            # a list of all the question attempts across all the sections of the test
            all_section_attempts = [section_attempt for section_attempt in
                test.test_attempts[0].section_attempts]

            total_test_score = 0

            for section_attempt in all_section_attempts:
                section_score = 0
                section_attempt.correct_question_count = 0
                section_attempt.incorrect_question_count = 0
                for question_attempt in section_attempt.question_attempts:
                    score, did_attempt, is_correct = question_attempt.calc_score_on_ques(
                            question_bank[question_attempt.question_id])

                    question_score = score
                    total_test_score += question_score

                    section_score += question_score

                    if should_persist:
                        question_attempt.was_correct = is_correct

                        if is_correct is True:
                            section_attempt.correct_question_count += 1
                        if is_correct is False:
                            section_attempt.incorrect_question_count += 1

                        if did_attempt:
                            question_attempt.score = score
                        else:
                            question_attempt.score = 0

                if should_persist:  # it will be committed later
                    section_attempt.score = section_score

            if should_persist:
                test.test_attempts[0].score = total_test_score
                test.test_attempts[0].is_complete = True

                if gradable_question_count == 0:
                    test.test_attempts[0].is_graded = True
                else:
                    pass
                    # print("going to add")

                test_attempt_id = test.test_attempts[0].id
                db.session.commit()

                TestAttempt.grade_code_cases.delay(
                        test_attempt_id)
                SixteenPReport.generate_report.delay(
                        test_attempt_id)

            return total_test_score

        except NoResultFound:
            return Error("Not Found", 404)()

    @staticmethod
    @celery.task()
    def grade_code_cases(test_attempt_id):
        """
        Grade a test attempt for coding questions.
        This assumes each question in the test has a question attempt for a user
        associated with it (see how test attempt setup works)


        :param test_attempt_id:
        :return:
        """
        from models import (CodingCase, SectionAttempt,
                            Question, QuestionAttempt)

        questions = (Question.query
                     .outerjoin(Question.coding_cases)
                     .join(Question.question_attempts)
                     .outerjoin(QuestionAttempt.chosen_language)
                     .join(SectionAttempt,
                           and_(
                                   SectionAttempt.id == QuestionAttempt.section_attempt_id,
                                   SectionAttempt.test_attempt_id == test_attempt_id))
                     .join(TestAttempt, and_(
                SectionAttempt.test_attempt_id == TestAttempt.id))
                     .options(
                contains_eager(Question.coding_cases).load_only(
                        CodingCase.points_wrong,
                        CodingCase.points_correct,
                        CodingCase.input,
                        CodingCase.right_output))
                     .options(
                contains_eager(Question.question_attempts).load_only(
                        QuestionAttempt.chosen_language_id,
                        QuestionAttempt.long_answer,
                        QuestionAttempt.correct_coding_cases_count,
                        QuestionAttempt.coding_average_time).contains_eager(
                        QuestionAttempt.section_attempt)
                    .contains_eager(
                        SectionAttempt.test_attempt))
                     .options(contains_eager(Question.question_attempts)
                              .contains_eager(QuestionAttempt.chosen_language))
                     # .filter(Question.type == QuestionTypesEnum.coding.value)
                     .all()
                     )

        test_attempt = (questions[0]
                        .question_attempts[0]
                        .section_attempt
                        .test_attempt)

        ##############################################################
        ##################### begin auto coding grading###############
        ##############################################################

        for question in questions:
            if question.type != "CODING":
                continue
            code = question.question_attempts[0].long_answer
            cases = question.coding_cases
            language_id = question.question_attempts[0].chosen_language_id
            inputs = [case.input for case in cases]
            language = question.question_attempts[0].chosen_language
            language = str(language).split(' ')[0].lower()

            # user didnt attempt this question
            if code is None or language_id is None:
                continue

            outputs, time_taken_arr, space_taken_arr = Externals.CaaS.get_outputs(
                    code,
                    language_id,
                    inputs)

            score = 0
            correct_outputs_count = 0
            time_taken_sum = 0

            for i, output in enumerate(outputs):

                if cases[i].right_output == output:
                    score += cases[i].points_correct

                    correct_outputs_count += 1
                    time_taken_sum += float(time_taken_arr[i])
                else:
                    # output was not perfect, try to do partial match

                    partial_match_score = (
                        compute_partial_match_score(output,
                                                    cases[i].right_output)
                    )

                    if partial_match_score == 0:
                        # partial match returned 0, deduct points from
                        # for the test case
                        score -= cases[i].points_wrong

                    else:
                        score += partial_match_score * cases[i].points_correct

            if test_attempt.score is None:
                test_attempt.score = 0

            test_attempt.score += score

            question.question_attempts[0].section_attempt.score += score
            question.question_attempts[0].score += score

            question.question_attempts[
                0].correct_coding_cases_count = correct_outputs_count

            if correct_outputs_count != 0:
                # average time taken by the code
                # in future can be replaced with max time taken
                question.question_attempts[
                    0].coding_average_time = time_taken_sum / correct_outputs_count

                # space used by the user's code
                question.question_attempts[
                    0].coding_max_space = max(space_taken_arr)

                # comment percentage used in code
                comment_length = 0
                code_length = float(len(code))
                # if language == "c":
                #     comment_length = len(TestAttempt.get_c_comments(code))
                # elif language == "c++":
                #     comment_length = len(TestAttempt.get_cpp_comments(code))
                # elif language == "java":
                #     comment_length = len(TestAttempt.get_java_comments(code))
                # elif language == "python":
                #     comment_length = len(TestAttempt.get_python_comments(code))
                # else:
                #     # handle default case here in else
                #     comment_length = 0
                # question.question_attempts[
                #     0].comment_to_code_ratio = comment_length / code_length

            if question.question_attempts[
                0].section_attempt.correct_question_count is None:
                question.question_attempts[
                    0].section_attempt.correct_question_count = 0

            if question.question_attempts[
                0].section_attempt.incorrect_question_count is None:
                question.question_attempts[
                    0].section_attempt.incorrect_question_count = 0

            if correct_outputs_count == len(outputs):
                question.question_attempts[
                    0].section_attempt.correct_question_count += 1

            else:
                question.question_attempts[
                    0].section_attempt.incorrect_question_count += 1

        ##############################################################
        ###################### end auto coding grading################
        ##############################################################

        regex = re.compile('<.*?>')
        # cleantext = re.sub(regex, '', )

        for question in questions:
            if question.type != "SUBJECTIVE":
                continue

            long_answer = question.question_attempts[0].long_answer
            if long_answer is None or long_answer.isspace():
                continue
            long_answer = re.sub(regex, ' ', str(long_answer))
            long_answer = re.sub(re.compile('&nbsp;'), ' ', str(long_answer))

            question.question_attempts[0].score = question.points_correct
            question.question_attempts[
                0].section_attempt.score += question.points_correct
            question.question_attempts[
                0].section_attempt.test_attempt.score += question.points_correct

            flagged_tokens = Externals.BingSpellCheck.get_spelling_flagged_tokens(
                    long_answer)
            if question.spelling_penalty is not None:
                total_penalty = len(
                        flagged_tokens) * question.spelling_penalty

                # total_penalty = random.uniform(6, 9)

                question.question_attempts[0].score -= total_penalty
                question.question_attempts[
                    0].section_attempt.score -= total_penalty
                question.question_attempts[
                    0].section_attempt.test_attempt.score -= total_penalty

            if len(flagged_tokens) == 0:
                question.question_attempts[
                    0].section_attempt.correct_question_count += 1
            else:
                question.question_attempts[
                    0].section_attempt.incorrect_question_count += 1

        test_attempt.is_graded = True
        db.session.commit()

        from models import TestAttemptReport

        TestAttemptReport.generate_report.delay(test_attempt_id)

        return

    # Extratcting comments from different file
    # functions are not finding the comment properly, need to update the logic
    # def get_java_comments(code):
    #     # Extracting Single line + MultipleLine Comments
    #     comment = re.findall(
    #             r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n]))*\*+/)|(//.*)", code)
    #     comments = ''.join(str(i) for i in comment)
    #
    #     return comments
    #
    # def get_c_comments(code):
    #     # Extracting MultipleLine Comments
    #     comment = re.findall(r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)",
    #                          code)
    #     comments = ''.join(str(i) for i in comment)
    #
    #     return comments
    #
    # def get_cpp_comments(code):
    #     # Extracting Single Line comments with //
    #     comment = re.findall(
    #             r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)", code)
    #     comments = ''.join(str(i) for i in comment)
    #
    #     return comments
    #
    # def get_python_comments(code):
    #     # Extracting Single Line comments with #
    #     comments = ''.join(str(i) for i in comment)
    #
    #     return comments
    #
    # def get_ruby_comments(code):
    #     # Extracting multiple and single line comments
    #     comment = re.findall(r"(\=begin[\w\W]*?=end)|(\#.*)", code)
    #     comments = ''.join(str(i) for i in comment)
    #
    #     return comments

    @staticmethod
    def analyse_16p(test_attempt_id):

        from models import Question
        from models import QuestionAttempt
        from models import SectionAttempt
        from Algos.SixteenP import scraping
        from models import Choice

        question_attempts = (QuestionAttempt.query
                             .join(QuestionAttempt.question)
                             .outerjoin(Question.choices)
                             .join(SectionAttempt,
                                   and_(
                                           SectionAttempt.id == QuestionAttempt.section_attempt_id,
                                           SectionAttempt.test_attempt_id == test_attempt_id))

                             .options(load_only(QuestionAttempt.choice_id))
                             .options(contains_eager(QuestionAttempt.question)
                                      .load_only(Question.id)
                                      .contains_eager(Question.choices)
                                      .load_only(Choice.id))
                             .all()
                             )

        scraping.scrape(question_attempts)
        return question_attempts
