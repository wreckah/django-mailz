from datetime import datetime

from celery import task
from django.conf import settings

from . import GETTERS, parse_email, render_email
from ..models import Account, Log
from ..tasks import send_message


@task
def respond():
    """
    Gets all not answered messages and creates tasks for sending answers.
    """
    for account in settings.MAILZ_AUTORESPOND_ACCOUNTS:
        if account['proto'] not in GETTERS:
            raise NotImplementedError(
                'Unsupported protocol "%s"' % account['proto']
            )

        last_check = Account.last_check(account)
        last_check.checked_at = datetime.now()

        for data, _ in GETTERS[account['proto']](account, last_check):
            # Data is: UID, body
            ctx = parse_email(data[1])

            already_answered = Log.objects.filter(
                account=last_check.account,
                message_id=ctx['message-id']
            ).exists()
            if already_answered:
                continue

            if account.get('preprocess'):
                ctx.update(account['preprocess'](ctx) or {})

            subject, body = render_email(
                ctx, account['template'], account['subject']
            )
            headers = {}
            if ctx['message-id']:
                headers['In-Reply-To'] = ctx['message-id']
                headers['References'] = ctx['references'] + \
                    (' ' if ctx['references'] else '') + ctx['message-id']
            send_message.delay(
                subject, body, account['from'], [ctx['to']], headers
            )

            Log(
                account=last_check.account,
                message_id=ctx['message-id']
            ).save()
#             if account.get('postprocess'):
#                 pass

        last_check.save()
