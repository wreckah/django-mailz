from email.utils import formataddr, parseaddr

from django import forms
from django.core.validators import validate_email

DEFAULT_TYPE = 'text/plain'


class NamedEmailField(forms.Field):

    def to_python(self, value):
        if not value:
            return ('', '')
        return parseaddr(value)

    def validate(self, value):
        super(NamedEmailField, self).validate(value)
        validate_email(value[1])

    def clean(self, value):
        return formataddr(super(NamedEmailField, self).clean(value))


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(max_length=50000)
    sender = NamedEmailField()
    recipient = NamedEmailField()
    content_type = forms.CharField()

    def clean(self):
        cleaned_data = super(TemplatedEmailForm, self).clean()
        if not cleaned_data.get('content_type'):
            cleaned_data['content_type'] = DEFAULT_TYPE
        return cleaned_data


class TemplatedEmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    template = forms.CharField(max_length=50000, required=False)
    template_name = forms.CharField(max_length=255, required=False)
    context = forms.CharField(max_length=50000)
    sender = NamedEmailField()
    recipient = NamedEmailField()
    content_type = forms.CharField()

    def clean(self):
        cleaned_data = super(TemplatedEmailForm, self).clean()
        if not cleaned_data.get('content_type'):
            cleaned_data['content_type'] = DEFAULT_TYPE

        if not (cleaned_data.get('template') or
                cleaned_data.get('template_name')):
            msg = 'Please, specify at least one of "template" or ' + \
                '"template_name" fields.'
            self._errors['template'] = self.error_class([msg])
        return cleaned_data
