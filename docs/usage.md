# Usage
To integrate Two-Factor Authentication (2FA) into your Django project using DRF_2FA, follow these simple steps:

## Message Based 2FA
**Applicable for `EmailOTPBackend`, `TwilioSMSBackend` or any Messaged based 2FA**

1. Add URL Pattern:

Incorporate the `drf_2fa` URLs into your Django project's urlpatterns:

```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('api/2fa/', include("drf_2fa.urls")),
    ...,
]
```
