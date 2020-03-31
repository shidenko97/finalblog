from threading import Thread

from flask import current_app
from flask_mail import Message

from blog import mail


def send_async_email(app, msg: Message):
    """
    Send in thread helper
    :param app: Current application instance
    :type app: LocalProxy
    :param msg: Generated email message
    :type msg: Message
    """

    with app.app_context():
        mail.send(msg)


def send_mail(recipients: list, subject: str, text: str, html: str):
    """
    Sending email with threads support
    :param recipients: List of recipients
    :type recipients: list
    :param subject: Subject of the message
    :type subject: str
    :param text: Message raw text
    :type text: str
    :param html: Message text in html format
    :type html: str
    """

    # Generate an email message
    msg = Message(subject=subject, recipients=recipients, body=text, html=html)

    # Send it in new thread
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
