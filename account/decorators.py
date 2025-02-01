from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def unauthorised(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:  
            return redirect('home_dash')  
        else:
            return view_func(request, *args, **kwargs)  
    return wrapper_func