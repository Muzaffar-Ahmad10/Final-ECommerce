from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def superuser_required(function):
    @wraps(function)
    @login_required
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Your are not Super Admin, So Please login before you visit this area of the site!')
            return redirect('login')
        return function(request, *args, **kwargs)
    
    return wrap
