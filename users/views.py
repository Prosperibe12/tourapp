from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
# function for register
def register(request):
    
    # prevent authenicated users from going to dashboard
    if request.user.is_authenticated:
        messages.warning(request, 'Already Logged In')
        redirect('dashboard')
        
    show = Userprofile()
    
    if request.method == 'POST':
        form = Userprofile(request.POST, request.FILES)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password1 = form.cleaned_data.get('password2')
            
            if User.objects.filter(username=username):
                messages.warning(request, 'Username already exist')
                return redirect('register')
            
            if User.objects.filter(email=email):
                messages.warning(request, 'Email already Exist')
                return redirect('register')
            
            if password != password1:
                messages.warning(request, 'Password do not Match')
                return redirect('register')
                
            user = User.objects.create_user(username, email, password)
            form = form.save(commit=False)
            form.user = user
            form.save()
            messages.success(request, 'Registered Successfully')
            
            # validate auth
            if "next" in request.GET:
                next_url = request.GET.get('next')
                return redirect(next_url)
            else:
                return redirect('loginuser')
        
    context = {
        'form': show,
        'Title': 'Register Page'
    }
    return render(request, 'users/register.html', context)

# function for login
def loginuser(request):
    
    if request.user.is_authenticated:
        messages.warning(request, 'Already Logged In')
        redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In Successfully')
            
            # check for authentication
            if "next" in request.GET:
                next_url = request.GET.get('next')
                return redirect(next_url)
            else:
                return redirect('index')
            
        else:
            messages.warning(request, 'Invalid Username or Password')
    
    context = {
        'Title': 'Login Page'
    }       
    return render(request, 'users/login.html', context)

# function to logout user
def logoutuser(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('loginuser')


# function to view dashboard

def dashboard(request):
    
    profile = request.user.customer
    context = {
        'Title': 'Dashboard',
        'profile': profile
    }
    return render(request, 'users/dashboard.html', context)


# function for updating user profile
def updateprofile(request):
    
    try:
        if not request.user.is_authenticated:
            messages.warning(request, 'Access Denied')
            return redirect('loginuser')
            
    except AttributeError:
        print("Login to continue")
    
    user = request.user.customer
    form = Updateprofile(instance=user)
    if request.method == 'POST':
        form = Updateprofile(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
    context = {
        'Title': 'Dashboard',
        'form': form
    }
    return render(request, 'users/updateprofile.html', context)