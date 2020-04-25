"""
Mail Module.

This handles sending emails using AWS SES.


Usage:
    1. create a folder for the email that you want to send
    2. create 3 files in the folder :
            html.html -> contains the html content of the email
            text.txt  -> contains the text content of the email
            subject   -> contains the subject of the email
        (all three support templating using jinja2)

    3. add a variable name in all caps , with the path of the template
        folder in the __init__.py of this module
        (see __init__.py for example)
    --------------This concludes setup process---------------

    Sending emails :

    from Mail import Mail,WELCOME_MAIL

    m = Mail('someemail@fakemail.com',
    html_data={'key':'value},
    text_data={'another_key':'another_value},
    subject_data={"key":"val"},
    template_root=WELCOME_MAIL) # this signifies email templates to use

    m.send()



"""

__author__ = "harshvardhan gupta"

import os.path as path

import boto3
import jinja2
from flask import current_app

from extensions import celery


class Mail:
    """
    Mail class.

    This does the setup required to send emails.

    See module usage for instructions on how to use.
    """

    CHARSET = "UTF-8"
    client = None
    data_args = {}

    def __init__(self, recipient,
                 subject_data,
                 html_data,
                 text_data,
                 template_root,
                 sender=None):
        """
        Set up an Email that can be sent later on

        :param recipient:       string -> email address of recipient
                                    or list of strings containing emails for each
        :param subject_data:      dict -> data for subject template
        :param html_data:         dict -> data for email template
        :param text_data:         dict -> data for HTML template
        :param template_root:   string -> Root Path of Template
        :param sender:          string -> email of sender By default, it uses
                                    the MAIL_DEFAULT_SENDER key from config
        """
        if not type(recipient) is list:
            recipient = [recipient]

        self.data_args['recipient'] = recipient
        self.data_args['subject_data'] = subject_data
        self.data_args['html_data'] = html_data
        self.data_args['text_data'] = text_data
        self.data_args['template_root'] = template_root
        self.data_args['sender'] = sender

        self.client = boto3.client(
                'ses',
                'us-east-1',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                aws_secret_access_key=current_app.config['AWS_SECRET_KEY'])

        if sender is None:
            self.sender = current_app.config['MAIL_DEFAULT_SENDER']
        self.recipient = recipient

        self.subject_data = subject_data
        self.html_data = html_data
        self.text_data = text_data

        self.html_template_path = path.join(template_root, 'html.html')
        self.text_template_path = path.join(template_root, 'text.txt')
        self.subject_path = path.join(template_root, 'subject.txt')

        self.jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(
                        path.dirname(self.subject_path)),
                undefined=jinja2.StrictUndefined
        )

    def _render_subject(self):
        """
        Render the subject template with the data provided

        :return: The rendered subject template
        """

        rendered_subject = self.jinja_env.get_template(
                path.basename(self.subject_path)) \
            .render(self.subject_data)

        return rendered_subject

    def _render_html(self):
        """
        Render the html template with the data provided

        :return: If the html template path exists, this returns the rendered
                template, else it returns None
        """

        if self.html_template_path:
            rendered_html = self.jinja_env.get_template(path.basename(
                    self.html_template_path)) \
                .render(self.html_data)

            return rendered_html

        return None

    def _render_text(self):
        """
        Render the text template with the data provided

        :return: If the text template path exists, this returns the rendered
                template, else it returns None
        """

        if self.text_template_path:
            rendered_text = self.jinja_env.get_template(
                    path.basename(self.text_template_path)) \
                .render(self.text_data)
            return rendered_text

        return None

    def send(self, deferred=True):
        """
        Sends the email to the recipient.

        This method calls the methods to render the emails, and then
        sends it.

        :return: None
        """
        if deferred:
            send_deferred_mail.delay(self.data_args)
            return

        body = {}

        # if html template path was supplied, add 'html'
        # key to to the email client
        rendered_html = self._render_html()

        if rendered_html:
            body['Html'] = {
                'Charset': self.CHARSET,
                'Data': rendered_html,
            }

        # if text template path was supplied, add 'text'
        # key to to the email client
        rendered_text = self._render_text()

        if rendered_text:
            body['Text'] = {
                'Charset': self.CHARSET,
                'Data': rendered_text,
            }

        if not rendered_text and not rendered_html:
            raise AttributeError("Rendered HTML and Rendered Text are both "
                                 "absent. Specify at least one of them")

        rendered_subject = self._render_subject()

        self.client.send_email(

                Destination={
                    'BccAddresses':
                        self.recipient
                },
                Message={
                    'Body': body,
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': rendered_subject,
                    },
                },
                Source=self.sender
        )


@celery.task()
def send_deferred_mail(args):
    Mail(**args).send(deferred=False)
