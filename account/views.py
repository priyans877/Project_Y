from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .decorators import unauthorised
from .models import Profile

# Create your views here.


@unauthorised
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirmpass')
               
        print(username)
        print(password ,confirm_pass)
        user = User.objects.filter(username = username)
        
        
        
        if confirm_pass== password:

            if user.exists():
                messages.error(request, 'Username already exists , Kindly Log In')
             
                # return render(request, 'account/register.html')   
            elif "@acem.edu.in" in email:
                messages.error(request , 'Kinldy register with College MailID')

            else:
                user = User.objects.create(
                    username = username,
                    first_name = firstname,
                    email = email
                )
                
                user.set_password(password)
                user.save()
                messages.success(request, 'User created successfully')

                return redirect('login')
        else:
            messages.error(request , "Make sure both Passwords or same")
               
    return render(request, 'account/register.html')
    
@unauthorised
def login_page(request):
    next_link = request.GET.get('next')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            return redirect('register')
        
        # if request.user.is_authenticated:
        #     return redirect('get_data')
        
        else:           
            print(username , password)
            user = authenticate(username = username, password = password)
            print(user)
            if user is None:
                messages.error(request, 'Invalid credentials')
                return render(request, 'account/login.html')
            else:
                login(request, user)
                print(next_link)
                if next_link ==None:
                    return redirect('home_dash')     
                else:
                    return redirect(next_link)         
    
    return render(request, 'account/login.html')



def logout_page(request):
    logout(request)
    return redirect('login')