from django.http import Http404
from django.contrib.auth.models import User


def check_user_exists(view_func):
    """Decorator to check if the user exists."""
    def _wrapped_view_func(request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func