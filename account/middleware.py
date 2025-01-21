import datetime
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        last_activity = request.session.get('last_activity')
        now = datetime.datetime.now()

        if last_activity:
            last_activity = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')
            inactivity_period = (now - last_activity).total_seconds()
            if inactivity_period > settings.SESSION_COOKIE_AGE:
                from django.contrib.auth import logout
                logout(request)
                return

        request.session['last_activity'] = now.strftime('%Y-%m-%d %H:%M:%S.%f')
