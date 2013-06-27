from celery import task
from django.core.mail import EmailMessage


@task
def send_message(subject, message, from_email, recipient_list, headers=None):
    msg = EmailMessage(
        subject, message, from_email, recipient_list, headers=headers
    )
    msg.send()
