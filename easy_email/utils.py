from django.template import Template as TemplateEngine
from easy_email.exceptions import TemplateNotFound
from easy_email.models import Template


def render_email_template(template_name, context=None, request=None, using=None):
    try:
        template = Template.objects.get(name=template_name)
    except:
        raise TemplateNotFound(f"Template `{template_name}` doesn't exist, please re-check the template_name.")
    
    template_engine = TemplateEngine(template_string=template.content, )
    email_content = template_engine.render(context, request)
    return email_content

