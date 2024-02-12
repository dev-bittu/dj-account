from django.shortcuts import redirect
from django.urls import reverse

def login_required(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_verified:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('account:login'))  # Redirect to the login page if user is not authenticated or not verified

    return wrap
