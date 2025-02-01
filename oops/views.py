from django.shortcuts import render

# Create your views here.


def under_dev(request):
    return render(request , 'account/under_dev.html')