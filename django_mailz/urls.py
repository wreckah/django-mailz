from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^send.json$', 'mailz.api.send'),
    url(r'^send_from_template.json$', 'mailz.api.send_from_template'),
)
