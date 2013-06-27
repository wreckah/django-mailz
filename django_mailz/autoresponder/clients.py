import imaplib


def _get_imap4(account, last_check):
    cls = imaplib.IMAP4_SSL if 'SSL' in account['proto'] else imaplib.IMAP4
    conn = cls(account['server'])
    conn.login(account['username'], account['password'])
    conn.select(readonly=1)  # INBOX is default

#     if last_check.checked_at:
#         search_args = (None, '(SINCE )')
#     else:
#         search_args = (None, 'ALL')
    _, data = conn.search(None, '(NOT SEEN)')
    messages = []
    for num in data[0].split():
        _, data = conn.fetch(num, '(UID RFC822)')
        messages.append(data)

    conn.close()
    conn.logout()

    return messages
