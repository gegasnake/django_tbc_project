from datetime import timedelta

from django.utils import timezone


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Define the time interval for updating
            now = timezone.now()
            last_active = request.user.last_active_datetime

            # Only update if more than a minute has passed
            if last_active is None or (now - last_active > timedelta(minutes=1)):
                request.user.last_active_datetime = now
                request.user.save(update_fields=['last_active_datetime'])

        response = self.get_response(request)
        return response


class InactivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            last_active = request.session.get('last_active')
            now = timezone.now()

            if last_active and (now - last_active).total_seconds() > 60:
                request.session.flush()
            else:

                request.session['last_active'] = now
        response = self.get_response(request)
        return response
