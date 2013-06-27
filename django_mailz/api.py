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
    print email.cleaned_data
    try:
        send_message.delay(
            email.cleaned_data['subject'],
            email.cleaned_data['message'],
            email.cleaned_data['sender'],
            [email.cleaned_data['recipient']]
        )
    except Exception as e:
        return error(unicode(e), 500)
    return response('ok')


@csrf_exempt
def send_from_template(request):
    email = TemplatedEmailForm(request.POST)
    if not email.is_valid():
        return error(email.errors, 400)

    ctx = loads(email.cleaned_data['context'])
    try:
        ctx = loads(email.cleaned_data['context'])
    except Exception as e:
        return error(unicode(e), 400)
    if email.cleaned_data.get('template'):
        message = render_string(email.cleaned_data['template'], ctx)
    else:
        message = render(email.cleaned_data['template_name'], ctx)

    try:
        send_message.delay(
            email.cleaned_data['subject'],
            message,
            email.cleaned_data['sender'],
            [email.cleaned_data['recipient']]
        )
    except Exception as e:
        return error(unicode(e), 500)
    return response('ok')
