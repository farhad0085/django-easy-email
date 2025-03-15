from django.views import View
from django.http import HttpResponse
from easy_email.processor import EmailProcessor
from easy_email.utils import render_email_template


class SendEmailAPIView(View):

    def get(self, request):
        # add two button (one for instant send, another for schedule)
        content = """
        <h2>Email sent</h2>
        """

        email_body = render_email_template('event_approval_email', {})
        print(email_body)

        EmailProcessor(
            subject="Test email subject",
            email_body="test email body",
            recipient_list=["farhad@assiduus.in"],
        )
        return HttpResponse(content)
