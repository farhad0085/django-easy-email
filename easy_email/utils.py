from django.template import Template as TemplateEngine, Context
from easy_email.exceptions import TemplateNotFound
from easy_email.models import Template


def render_email_template(template_name, context=None, request=None):
    try:
        template = Template.objects.get(name=template_name)
    except:
        raise TemplateNotFound(template_name)
    
    template_engine = TemplateEngine(template_string=template.content)
    context = Context({'request': request, **context })
    email_content = template_engine.render(context)
    return email_content

