from flask import current_app as app, redirect, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, URLSafeSerializer
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound

from Mail import FORGOT_PASSWORD, Mail, SIGNUP_ACTIVATION, WELCOME_MAIL
from Sugar import JSONifiedNestableBlueprint, requires_validation
from controllers.rex import CookieHelper
from extensions import bcrypt, celery, db, mautic
from models import Corporate, Error, User
from .req_val import ChangePasswordInputs, ForgotPasswordInputs, LoginInputs, \
    ResendActivationInputs, ResetPasswordInputs, SignupInputs

user_controller = JSONifiedNestableBlueprint('User', __name__)


@user_controller.route('/user', methods=['GET'])
@login_required
def get_user():
    """
    Current User is determined by Flask Login based on the Session Cookie

    :return:
    """
    # print(session)

    fields = [c.name for c in User.__table__.c]

    # get all fields except
    fields = filter(lambda x: x not in ['password', 'is_active', 'type'],
                    fields)


    user = (User.query
            .outerjoin(User.college)
            .outerjoin(User.corporate)
            .outerjoin(Corporate.tests)
            .filter(User.id == current_user.id)
            .options(contains_eager(User.college))
            .options(contains_eager(User.corporate)
                     .contains_eager(Corporate.tests))
            .options(load_only(*fields))
            .one()
            )

    # the current anonymous merging algorithm has bugs and has been
    # commented for future consideration

    # if "mtc_id" in request.cookies:
    #     anon_id = request.cookies['mtc_id']
    #     merge_anonymous_user.apply_async(args=(anon_id, user.email),
    #                                      countdown=25)

    return user


@celery.task()
def merge_anonymous_user(anon_id, email):
    mautic.API.contacts.merge_anon_contact_with_email(anon_id=anon_id,
                                                      email=email)


@user_controller.route('/user/login', methods=['POST'])
@requires_validation(LoginInputs)
def user_login():
    """
    Converts password text to hash string using bcrypt, verifies the
    combination against the database and creates a session for user in Flask
    :param email:
    :param password:
    :return: user.todict()
    """
    req = request.get_json()
    user = (User.query
            .filter(User.email == req['email'])
            .first()
            )
    if user is not None:
        if bcrypt.check_password_hash(user.password, req['password']):
            if user.is_active == False:
                return Error("Email not confirmed. Please check your mail",
                             http_code=403)()

            login_user(user)
            session.permanent = True

            # get all fields except
            fields = [c.name for c in User.__table__.c]
            fields = filter(
                    lambda x: x not in ['password', 'is_active', 'type'],
                    fields)
            fields = list(fields)
            fields.append("corporate")
            fields.append({"corporate": ["tests", "name", "id"]})

            json_dict = user.todict(fields)

            if json_dict['corporate'] != None:
                corporate_id = json_dict['corporate']['id']
                CookieHelper.set_corporate_cookie(corporate_id)

            return user.todict(fields)
    return Error("Invalid Email or Password", 401)()


@user_controller.route('/user/logout', methods=['POST'])
@login_required
def user_logout():
    """
    Terminates session for an User in Flask based on the cookie sent in the
    request
    :return:
    """
    logout_user()
    session.clear()
    return ""


### BUG!!!
### An invalid college id causes a 500 error

@user_controller.route('/user/signup', methods=['POST'])
@requires_validation(SignupInputs)
def signup_user():
    """
    Checks if Email already exists in database otherwise, creates an account
    for the User
    :param  email:
    :param  name:
    :param  password:
    :param  phone_no:
    :return:
    """
    req = request.get_json()

    req['password'] = bcrypt.generate_password_hash(req['password'])

    user_exists = db.session \
        .query(User.query.filter(User.email == req['email']).exists()) \
        .scalar()

    if user_exists:
        return Error("User exists", 400)()

    del req['captcha_token']
    user = User(**req)

    db.session.add(user)

    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    activation_token = serializer.dumps(user.email)

    activation_url = url_for('User.activate_user',
                             activation_token=activation_token,
                             _external=True)

    db.session.commit()

    # if mautic works , then we will deleted this code block

    # Mail(req['email'],
    #      subject_data={'name': req['full_name']},
    #      html_data={'token': activation_url},
    #      text_data={'name': req['full_name']},
    #      template_root=SIGNUP_ACTIVATION
    #      ).send()

    add_user_to_mautic.delay(req['full_name'], req['email'], req['phone_no'],
                             user.created_date, user.referral_code_used,
                             user.graduation_date,
                             user.branch,
                             user.degree,
                             activation_url=activation_url)

    return ""


@celery.task()
def add_user_to_mautic(full_name,
                       email,
                       phone,
                       join_date,
                       referral_code_used,
                       graduation_date,
                       branch,
                       degree,
                       activation_url):
    """
    Add the user to mautic.
    After that , add send a verification email to him

    :param full_name:
    :param email:
    :param phone:
    :param join_date:
    :param referral_code_used:
    :param graduation_date:
    :param branch:
    :param degree:
    :param activation_url:
    :return:
    """
    college = (User.query.filter(User.email == email).one()).college

    college_name = college.college_name if college is not None else None

    mautic.API.contacts.create_contact(firstname=full_name,
                                       lastname=None,
                                       email=email,
                                       college_name=college_name,
                                       phone=phone,
                                       join_date=join_date,
                                       is_active=False,
                                       referral_code_used=referral_code_used,
                                       graduation_date=graduation_date,
                                       degree=degree,
                                       branch=branch)

    mautic.send_activation_email(email, activation_url)


@user_controller.route('/user/activate/<path:activation_token>', methods=[
    'GET'])
def activate_user(activation_token):
    """
    Activate a particular user, based on activation token.
    This sets the is_active field to true in the db.
    :param activation_token: the token that user should have in email
    :return: 403 if any errors, else redirect to root  , and user is activated
    """
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])

    try:
        email = serializer.loads(
                activation_token
        )
        user = User.query \
            .filter(User.email == email) \
            .one()

        user.is_active = True
        db.session.commit()

        # Mail(user.email,
        #      subject_data={'name': user.full_name},
        #      html_data={'name': user.full_name},
        #      text_data={'name': user.full_name},
        #      template_root=WELCOME_MAIL
        #      ).send()

        activate_user_to_mautic.delay(user.email)

        return redirect(f"{request.url_root}login")

    except (NoResultFound, BadSignature):
        return Error('Invalid Token', 403)()


@celery.task()
def activate_user_to_mautic(email):
    mautic.API.contacts.create_contact(firstname=None,
                                       lastname=None,
                                       email=email,
                                       college_name=None,
                                       phone=None,
                                       join_date=None,
                                       is_active=True)


@user_controller.route('/user/forgot_password', methods=['POST'])
@requires_validation(ForgotPasswordInputs)
def forgot_password():
    """
    Sends Reset Password link to User's email address. User can change
    his/her password through the link mentioned in the Email. It won't be an
    endpoint, it will be a webpage
    :return: 403 if any errors, else return 200
    """
    req = request.get_json()

    serializer = URLSafeSerializer(app.config['SECRET_KEY'])

    try:
        user = User.query \
            .filter(User.email == req['email']) \
            .filter(User.is_active) \
            .one()

        token = serializer.dumps(req['email'])
        reset_password_link = f"{request.url_root}reset_password?token={token}"

        Mail(user.email,
             subject_data={'name': user.full_name},
             html_data={'token': reset_password_link},
             text_data={'token': reset_password_link},
             template_root=FORGOT_PASSWORD
             ).send()

        return ""
    except NoResultFound:
        return Error('Invalid Email Address', 403)()


@user_controller.route('/user/reset_password/<path:reset_token>', methods=[
    'POST'])
@requires_validation(ResetPasswordInputs)
def reset_password(reset_token):
    """
    Validates Reset Token and Updates the Password in the Database
    :param reset_token:
    :return: 403 if any errors, else return 200
    """
    req = request.get_json()
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])

    try:
        email = serializer.loads(reset_token)

        user = User.query \
            .filter(User.email == email) \
            .filter(User.is_active) \
            .one()

        user.password = bcrypt.generate_password_hash(req['new_password'])
        db.session.commit()

        return ""
    except NoResultFound:
        return Error('Invalid Reset Token', 403)()


@user_controller.route('/user/change_password', methods=['POST'])
@requires_validation(ChangePasswordInputs)
@login_required
def change_password():
    """
    Allows User to change Password after validating the Old Password. User
    must be logged in to be able to do this.
    :return: 403 if old password doesn't match, 400 if any error, else 200
    """
    req = request.get_json()

    try:
        user = User.query \
            .filter(User.id == current_user.id) \
            .filter(User.is_active) \
            .one()

        if bcrypt.check_password_hash(user.password, req['old_password']):
            user.password = bcrypt.generate_password_hash(req['new_password'])
            db.session.commit()
            return ""

        return Error('Invalid Old Password', 403)
    except NoResultFound:
        return Error('Invalid User', 400)()


@user_controller.route('/user/resend_activation', methods=['POST'])
@requires_validation(ResendActivationInputs)
def resend_activation():
    """
    Resend the activation token in the user's email.
    returns: 403 if any errors occur. 200 if successful, and user get the
             activation mail resent to him.
    """
    req = request.get_json()

    try:
        user = (User.query
                .filter(User.email == req['email'])
                .one())

        if user.is_active:
            return Error("User is already active", 403)()

        serializer = URLSafeSerializer(app.config['SECRET_KEY'])
        activation_token = serializer.dumps(user.email)

        activation_url = url_for('User.activate_user',
                                 activation_token=activation_token,
                                 _external=True)

        Mail(req['email'],
             subject_data={'name': user.full_name},
             html_data={'token': activation_url},
             text_data={'name': user.full_name},
             template_root=SIGNUP_ACTIVATION
             ).send()

        return ""
    except NoResultFound:
        return Error("User with that email doesnt exist", 403)()
