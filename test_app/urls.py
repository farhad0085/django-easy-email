from django.urls import path
from test_app.views import SendEmailAPIView


urlpatterns = [
    path('send/', SendEmailAPIView.as_view()),
]