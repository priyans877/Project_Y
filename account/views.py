from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .decorators import unauthorised
from .models import Profile , AuthEmail


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
            elif "@acem.edu.in" not in email:
                messages.error(request , 'Kinldy register with College MailID')

            elif not AuthEmail.objects.filter(emails=email.lower()).exists():
                messages.error(request,"You'r not a Teacher")
            
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
        email_get = request.POST.get('username')
        password = request.POST.get('password')
        username = ""
        
        
        if "@" not in email_get:
            if not User.objects.filter(username=email_get).exists():
                messages.error(request, 'User Not Register - Kindly Register')
                return redirect('register') 
            
            
            username = email_get
            pass
        
        elif "@" in email_get:
            if "@acem.edu.in" not in email_get:
                messages.error(request , "Kindly register with College MailID")
                return redirect('login')
            
            else:
                if not User.objects.filter(email=email_get).exists():
                    messages.error(request, 'User Not Register - Kindly Register')
                    return redirect('register')
                else:
                    username = User.objects.get(email__iexact = email_get).username
        
     
        if username:          
            print(email_get, password)
   
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

