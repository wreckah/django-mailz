django-mailz
============

Autoresponder and sending emails queuing by django-celery.

Setting up autoresponder in settings.py:

    BROKER_URL = 'django://'
    # Import to register the task. I don't know how to fo it properly.
    from django_mailz.autoresponder.tasks import respond
    CELERYBEAT_SCHEDULE = {
        'check_new_mailz': {
            'task': 'django_mailz.autoresponder.tasks.respond',
            'schedule': timedelta(seconds=60),
        },
    }
    CELERY_TIMEZONE = 'UTC'
    setup_loader()

    MAILZ_AUTORESPOND_ACCOUNTS = [
        {
            'server': 'imap.yandex.ru',
            'proto': IMAP4_SSL,
            'username': 'username@doman.com',
            'password': 'password123',
            'template': 'my_app/autoresponse.html',
            'subject': 'Re: {{subject}}',
            'from': 'John Doe <johndoe@doman.com>',
            'preprocess': lamda x: x,
            'postprocess': lambda y: y,
        }
    ]

Adding sending e-mail message into the queue:

    from django_mailz.tasks import send

    send.delay(
        'subject',
        'body',
        'from@domain.com',
        ['to@domain.com'],
        {'X-Header': 'Value'}
    )
