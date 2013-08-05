from celery import task
from django.core.mail import EmailMessage


@task
def send_message(subject, message, from_email, recipient_list, headers=None,
                 content_type=None):
    msg = EmailMessage(
        subject, message, from_email, recipient_list, headers=headers
    )
    if content_type:
        if '/' in content_type:
            content_type = content_type.split('/')[1]
        msg.content_subtype = content_type
    msg.send()
