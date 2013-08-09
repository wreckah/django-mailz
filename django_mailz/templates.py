from django.template.base import TemplateDoesNotExist
from django.template.context import Context
from django.template.loader import get_template, get_template_from_string


class RenderError(Exception):
    pass


def render(template, context):
    ctx = Context(context)
    # TODO: cache templates
    try:
        tpl = get_template(template)
    except TemplateDoesNotExist as e:
        raise RenderError('Couldn\'t load template %s' % e)
    return tpl.render(ctx)


def render_string(template, context):
    ctx = Context(context)
    # TODO: cache templates
    return get_template_from_string(template).render(ctx)
