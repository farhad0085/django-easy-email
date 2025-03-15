from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader
from django.template.base import Origin
from easy_email.models import Template


class DatabaseTemplateLoader(BaseLoader):

    def get_template_sources(self, template_name):
        origin = Origin(template_name, template_name=template_name)
        return [origin]

    def get_contents(self, template_name):
        try:
            # Try to get the template content from the database
            template = Template.objects.get(name=template_name)
            return template.content
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)
