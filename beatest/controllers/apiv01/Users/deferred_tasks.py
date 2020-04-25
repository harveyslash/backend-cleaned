from extensions import celery, mautic
from models import User


# @celery.task()
def create_mautic_contact_from_user(user_id):
    user = (User.query
            .filter(User.id == user_id)
            .one())

    # mautic.API.contacts.
    pass
