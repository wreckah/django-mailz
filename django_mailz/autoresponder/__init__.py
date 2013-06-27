from email.header import decode_header
from email.parser import Parser
from email.utils import formataddr, parseaddr

from .. import IMAP4, IMAP4_SSL
from ..autoresponder.clients import _get_imap4
from ..templates import render, render_string


parser = Parser()


def decode_header_string(header):
    return ''.join([
        chunk[0].decode(chunk[1] or 'ascii', 'ignore')
        for chunk in decode_header(header)
    ])


def parse_email(message):
    msg = parser.parsestr(message)
    name, email = parseaddr(msg['from'])
    return {
        'subject': decode_header_string(msg['subject']),
        'name': decode_header_string(name),
        'email': email,
        'to': formataddr((name, email)),
        'message-id': msg.get('message-id', '').strip(),
        'references': msg.get('references', '').strip(),
    }


def render_email(context, template, subject_template=None):
    if subject_template:
        subject = render_string(subject_template, context)
    else:
        subject = 'Re: ' + context['subject']
    body = render(template, context)
    return subject, body


GETTERS = {
    IMAP4: _get_imap4,
    IMAP4_SSL: _get_imap4,
}
