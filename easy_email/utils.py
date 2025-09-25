
from django.template import Template as TemplateEngine, Context
from easy_email.exceptions import TemplateNotFound
from easy_email.models import Template


def render_email_template(template_name, context=None, request=None):
    """
    Render an email template stored in the database using Django's template engine.

    This function looks up a `Template` object by its `name` field, compiles its
    `content` into a Django `Template`, and renders it with the provided context.
    It is designed to generate dynamic email content.

    Args:
        template_name (str): The name of the template to retrieve from the database.
        context (dict, optional): A dictionary of context variables to pass to the
            template. Defaults to an empty dictionary.
        request (HttpRequest, optional): An optional Django request object, which
            will be included in the template context under the key `'request'`.

    Returns:
        email_content (str): The rendered email content as a string.

    Raises:
        TemplateNotFound: If no template with the given `template_name` exists.
    """
    try:
        template = Template.objects.get(name=template_name)
    except:
        raise TemplateNotFound(template_name)
    
    template_engine = TemplateEngine(template_string=template.content)
    context = Context({'request': request, **context })
    email_content = template_engine.render(context)
    return email_content

