from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from easy_email.processor import DefaultEmailProcessor
from easy_email.utils import render_email_template


class SendEmailAPIView(View):

    def get(self, request):
        # Render the template with buttons to either send or schedule the email
        return render(request, 'test_app/send_email.html')
    
    def post(self, request):
        action = request.POST.get('action')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        body = render_email_template('test_extended2', {})
        # Get the recipients from the form
        recipients = request.POST.get('recipient', '').split(',')
        recipients = [email.strip() for email in recipients]
        
        if action == 'send_instantly':
            # Logic to send email instantly
            email = DefaultEmailProcessor(
                subject=subject,
                email_body=body,
                recipient_list=recipients,
            )
            email.send()
            return JsonResponse({'message': 'Email sent instantly!'})
        
        elif action == 'schedule':
            # Logic to schedule the email
            scheduled_time = request.POST.get('scheduled_time')
            if scheduled_time:
                scheduled_time = timezone.make_aware(scheduled_time)  # Convert to timezone-aware datetime
                # TODO: Logic to schedule email
                return JsonResponse({'message': f'Email scheduled for {scheduled_time}'})
        
        return JsonResponse({'error': 'Invalid action'}, status=400)
