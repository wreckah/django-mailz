from json import dumps, loads

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import EmailForm, TemplatedEmailForm
from .tasks import send_message
from .templates import render, render_string


def response(data):
    return HttpResponse(dumps(data), content_type='application/json')


def error(message, code=500):
    return HttpResponse(
        dumps(message),
        status=code,
        content_type='application/json'
    )


@csrf_exempt
def send(request):
    email = EmailForm(request.POST)
    if not email.is_valid():
        return error(email.errors, 400)

    data = email.cleaned_data
    try:
        send_message.delay(
            data['subject'],
            data['message'],
            data['sender'],
            [data['recipient']],
            {'Content-Type': data['content_type']}
        )
    except Exception as e:
        return error(unicode(e), 500)

    return response('ok')


@csrf_exempt
def send_from_template(request):
    email = TemplatedEmailForm(request.POST)
    if not email.is_valid():
        return error(email.errors, 400)

    data = email.cleaned_data
    ctx = loads(data['context'])
    try:
        ctx = loads(data['context'])
    except Exception as e:
        return error(unicode(e), 400)
    if data.get('template'):
        message = render_string(data['template'], ctx)
    else:
        message = render(data['template_name'], ctx)

    try:
        send_message.delay(
            data['subject'],
            message,
            data['sender'],
            [data['recipient']],
            {'Content-Type': data['content_type']}
        )
    except Exception as e:
        return error(unicode(e), 500)

    return response('ok')
