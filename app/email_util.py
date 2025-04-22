from flask_mail import Message
from flask import current_app
from . import mail


def send_inquiry_notification(inquiry):
    if not current_app.config.get('MAIL_USERNAME'):
        # mail not configured
        return
    msg = Message(subject=f"New Inquiry: {inquiry.subject}",
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[current_app.config['MAIL_USERNAME']])
    msg.body = f"""Name: {inquiry.name}\nEmail: {inquiry.email}\nPhone: {inquiry.phone}\n---\n{inquiry.message}"""
    mail.send(msg)