from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from .forms import CustomerUserCreationForm, CustomUserAuthenticationForm # custom user creation forms
from .models import CustomUser
from django.contrib import messages 
from django.core.mail import EmailMessage # send_mail # to send the mail after successful email creation
from django.conf import settings

# Create your views here.
# User creation
def user_creation_view(request):
    """Creates the user account"""
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST) # initialize the form
        if form.is_valid():
            form.save()
            # Successful creation
            # send the email
            try:
                email_message = EmailMessage(
                    "Welcome to PATA", # subject
                    "Lost a loved one? We would do our best in helping you find them. Upload their details, and you will be notified just as soon as anyone identifies them", # message
                    settings.EMAIL_HOST_USER, # from who?
                    [form.instance.email], # the email of the user
                )
                email_message.send() # send the email
            except Exception as e:
                raise Exception("Email sending failed {}".format(str(e)))
            
            messages.success(request, 'Account created successful. You can now log in with your details')
            # return redirect('accounts:login') # take back to login page
            return HttpResponse('Registration successful')
        else:
            messages.error(request, 'Oops! Something went wrong. Try again later')
    else:
        form = CustomerUserCreationForm()
    
    # The template
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

# Authentication/login view
def authentication_view(request):
    """Login/Authenticate the user"""
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() # how to pick the user details
            login(request, user)
            messages.success(request, 'Welcome!')
            return redirect('accounts:home')
        else:
            messages.error(request, 'Login unsuccesful, please try again')
        
    else:
        form = CustomUserAuthenticationForm()
    
    # The template
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

# logout view
def logout_user(request):
    """Logout user"""
    logout(request)
    # success message
    return HttpResponse('Succesfull logout')
    # the template

# the home page
def home(request):
    """The landing page"""
    context = {}
    return render(request, 'common/index.html', context)