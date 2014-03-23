# django-mailz

Autoresponder and sending emails from queue by django-celery.

## Autoresponder

Set up the autoresponder in settings.py:
```py
BROKER_URL = 'django://'
# Import to register the task. I don't know how to do it properly.
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
        'server': 'imap.domain.com',
        'proto': 'django_mailz.IMAP4_SSL',
        'username': 'username@domain.com',
        'password': 'password123',
        'template': 'my_app/autoresponse.html',
        'subject': 'Re: {{subject}}',
        'from': 'John Doe <johndoe@domain.com>',
        'preprocess': lamda x: x,
        'postprocess': lambda y: y,
    }
]
```

## Messages queue

Add e-mail message into the queue:
```py
from django_mailz.tasks import send

send.delay(
    'subject',
    'body',
    'from@domain.com',
    ['to@domain.com'],
    {'X-Header': 'Value'}
)
```

## HTTP REST API

Turn on API in urls.py:
```py
urlpatterns = patterns('',
    ...
    url(r'^api/mailz/', include('django_mailz.urls')),
)
```

Run server:
```sh
python manage.py runserver 127.0.0.1:8089
```

Send email message:
```sh
curl -d 'message=Hello, world!&subject=Test message&recipient=john@doe.com&sender=jane@doe.com' \
'http://127.0.0.1:8089/api/mailz/send.json'
```

Render Django-template and send e-mail message:
```sh
curl -d 'template=Hello, {{ name }}!&context={"name":"John Doe"}&subject=Test message&recipient=john@doe.com&sender=jane@doe.com' \
'http://127.0.0.1:8089/api/mailz/send_from_template.json'
```

Or render template from filesystem:
```sh
curl -d 'template_name=myapp/email.html&context={"name":"John Doe"}&subject=Test message&recipient=john@doe.com&sender=jane@doe.com&content_type=text/html' \
    'http://127.0.0.1:8089/api/mailz/send_from_template.json'
```
