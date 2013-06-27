from django.db import models


class Account(models.Model):
    account = models.CharField(max_length=255, unique=True)  # username@server
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get(cls, account_id):
        try:
            acc = cls.objects.get(account=account_id)
        except cls.DoesNotExist:
            acc = cls(account=account_id)
            acc.save()
        return acc

    @classmethod
    def last_check(cls, account):
        if isinstance(account, cls):
            acc = account
        elif hasattr(account, 'items'):
            acc = cls.get('%(username)s@%(server)s' % account)
        else:  # Supposed that account is string.
            acc = cls.get(account)
        try:
            last_check = LastCheck.objects.get(account=acc)
        except LastCheck.DoesNotExist:
            last_check = LastCheck(account=acc)
        return last_check


class LastCheck(models.Model):
    account = models.ForeignKey(Account, unique=True)
    checked_at = models.DateTimeField(auto_now=True)


class Log(models.Model):
    message_id = models.CharField(max_length=255)
    account = models.ForeignKey(Account)
    responded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('message_id', 'account'),)
