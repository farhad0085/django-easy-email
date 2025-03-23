from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from easy_email.models import Attachment
from easy_email.processor import CeleryEmailProcessor, DefaultEmailProcessor
from easy_email.utils import render_email_template


class SendEmailAPIView(View):

    def get(self, request):
        # Render the template with buttons to either send or schedule the email
        return render(request, 'test_app/send_email.html')
    
    def post(self, request):
        action = request.POST.get('action')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        body = render_email_template('test', {})
        files = Attachment.objects.all()
        # Get the recipients from the form
        recipients = request.POST.get('recipient', '').split(',')
        recipients = [email.strip() for email in recipients]
        
        if action == 'send_instantly':
            # Logic to send email instantly
            email = DefaultEmailProcessor(
                subject=subject,
                email_body=body,
                recipient_list=recipients,
                files=files
            )
            email.send()
            return JsonResponse({'message': 'Email sent instantly!'})
        else:
            # Logic to schedule email
            email = CeleryEmailProcessor(
                subject=subject,
                email_body=body,
                recipient_list=recipients,
                files=files
            )
            email.send(send_time=50)
            return JsonResponse({'message': 'Email scheduled successfully!'})
