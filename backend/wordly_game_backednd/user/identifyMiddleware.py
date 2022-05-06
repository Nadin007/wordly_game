from django.http import HttpRequest
from .models import User


def identify_middleware(get_response):
    def middleware(request: HttpRequest):
        if not request.user.is_authenticated:
            usr_token = request.COOKIES.get('logged_in')
            print(usr_token)
            if usr_token:
                try:
                    request.user = User.objects.get(user_token=usr_token)
                except Exception:
                    pass

        return get_response(request)
    return middleware
