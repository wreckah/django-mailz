from django.template.base import TemplateDoesNotExist, TemplateSyntaxError
from django.template.context import Context
from django.template.loader import get_template, get_template_from_string


class RenderError(Exception):
    pass


def render(template, context):
    ctx = Context(context)
    try:
        # TODO: cache templates
        tpl = get_template(template)
        return tpl.render(ctx)
    except TemplateDoesNotExist as e:
        raise RenderError('Couldn\'t load template %s' % e)
    except TemplateSyntaxError as e:
        raise RenderError('Syntax error in template: %s' % e)


def render_string(template, context):
    ctx = Context(context)
    try:
        # TODO: cache templates
        return get_template_from_string(template).render(ctx)
    except TemplateSyntaxError as e:
        raise RenderError('Syntax error in template: %s' % e)
