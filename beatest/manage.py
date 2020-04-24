"""
Entry Point of the app.

Usage:
    FLASK_APP=manage.py flask run

Also has custom commands

Scripts that are required for functioning of the app itself should go here.

"""
import click
from celery.bin.celery import main as celery_main
from sqlalchemy.orm import contains_eager, load_only
from tqdm import tqdm

from extensions import db, mautic, bcrypt
from models import Test
from scripts.generate_hashed_passes import get_hashed_passes_csv
from scripts.migrate_question_attempt_redundant import \
    migrate_question_attempt_was_correct_command
from scripts.migrate_sections_to_many_to_many import \
    migrate_sections_to_many_to_many_command
from scripts.persist_sectional_scores import persist_section_scores_command
from wsgi import app


@app.cli.command()
def run_celery_worker():
    """Start the celery Worker"""

    celery_args = ['celery', 'worker']
    with app.app_context():
        celery_main(celery_args)


@app.cli.command()
def run_celery_beat():
    """Start the celery beat"""

    celery_args = ['celery', 'beat', '--pidfile', '/tmp/beat.pid']
    with app.app_context():
        celery_main(celery_args)


@app.cli.command()
@click.argument('input_csv')
@click.argument('output_csv')
def get_hashed_passwords(input_csv, output_csv):
    """
    Get hashes for a csv of plaintext passwords.

    :param input_csv:
    :param output_csv:
    :return:
    """
    with app.app_context():
        get_hashed_passes_csv(input_csv, output_csv)


@app.cli.command()
def persist_section_scores():
    """
    """
    with app.app_context():
        persist_section_scores_command()


@app.cli.command()
def migrate_sections():
    """
    """
    with app.app_context():
        migrate_sections_to_many_to_many_command()


@app.cli.command()
def migrate_question_attempt_was_correct():
    """
    """
    with app.app_context():
        migrate_question_attempt_was_correct_command()


@app.cli.command()
def migrate_to_allow_jumps():
    """
    """
    with app.app_context():
        for test in tqdm(Test.query.all()):
            if test.type == "CAT":
                test.allow_section_jumps = False
            else:
                test.allow_section_jumps = True

        db.session.commit()


@app.cli.command()
def push_to_mautic():
    from models import User, College

    with app.app_context():
        users = (User.query
                 .outerjoin(User.college)
                 .options(contains_eager(
                User.college
        ).load_only(College.college_name))

                 .options(load_only(User.email,
                          User.full_name,
                          User.phone_no,
                          User.is_active,
                          User.created_date
                          ))
                 .all())

        for user in tqdm(users):
            college = user.college.college_name if user.college is not None else None

            mautic.API.contacts.create_contact(firstname=user.full_name,
                                               lastname=None,
                                               email=user.email,
                                               phone=user.phone_no,
                                               is_active=user.is_active,
                                               join_date=user.created_date,
                                               college_name=college)


@app.cli.command()
@click.argument('password')
def get_hash_for_pass(password):
    with app.app_context():
        password = bcrypt.generate_password_hash(password).decode()
        print(password)
