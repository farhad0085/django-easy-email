from django.views import View
from django.http import HttpResponse


class SendEmailAPIView(View):

    def get(self, request):
        content = """
        <h2>Email sent</h2>
        """
        return HttpResponse(content)
