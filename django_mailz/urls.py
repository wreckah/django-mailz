from django.conf.urls import patterns, url

urlpatterns = patterns(
    'django_mailz.api',
    url(r'^send.json$', 'send'),
    url(r'^send_from_template.json$', 'send_from_template'),
)
