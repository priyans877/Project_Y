from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class unauthorised(view_func):
    def wrapper_func(request , *args, **kwargs):
        if request.user.authenticated() == None:
            return redirect('home_scrap')
        else:
            return redirect("login")
        