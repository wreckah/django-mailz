from django.template.context import Context
from django.template.loader import get_template, get_template_from_string


def render(template, context):
    ctx = Context(context)
    # TODO: cache templates
    return get_template(template).render(ctx)


def render_string(template, context):
    ctx = Context(context)
    # TODO: cache templates
    return get_template_from_string(template).render(ctx)
