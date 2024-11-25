from django.views import View
from django.http import HttpResponse
from easy_email.processor import EmailProcessor


class SendEmailAPIView(View):

    def get(self, request):
        content = """
        <h2>Email sent</h2>
        """

        EmailProcessor(
            subject="Test email subject",
            email_body="test email body",
            recipient_list=["farhad@assiduus.in"],
        )
        return HttpResponse(content)
