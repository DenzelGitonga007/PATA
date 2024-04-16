from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import CustomerUserCreationForm, CustomUserAuthenticationForm # custom user creation forms
from .models import CustomUser
from posts.models import MissingPerson
from django.contrib import messages 
from django.core.mail import EmailMessage # send_mail # to send the mail after successful email creation
from django.conf import settings
from .forms import CustomerUserCreationForm, CustomUserAuthenticationForm
from .models import CustomUser, UserProfile

# User creation
def user_creation_view(request):
    """Creates the user account"""
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST) # initialize the form
        if form.is_valid():
            user = form.save()
            # UserProfile.objects.create(user=user)  # Create UserProfile for the new user
            user_email = form.cleaned_data.get('email') # get the user's email
            # Successful creation
            # send the email
            try:
                email_message = EmailMessage(
                    "Welcome to PATA", # subject
                    "Lost a loved one? We would do our best in helping you find them. Upload their details, and you will be notified just as soon as anyone identifies them", # message
                    settings.EMAIL_HOST_USER, # from who?
                    [user_email], # the email of the user
                )
                email_message.send() # send the email
            except Exception as e:
                raise Exception("Email sending failed {}".format(str(e)))
            
            messages.success(request, 'Account created successful. You can now log in with your details')
            return redirect('accounts:login') # take back to login page
            
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
            return redirect('posts:posts_index')
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


# The User's profile
@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    followers = profile_user.following_me.all()
    following = profile_user.following_them.all()
    # Get posts related to the user if you have a post model
    # posts = profile_user.posts.all()
    posts = MissingPerson.objects.filter(user_id=user_id).order_by('-created_at')

    context = {
        'profile_user': profile_user,
        'following': following,
        'followers': followers,
        'posts': posts,
    }
    return render(request, 'accounts/profile.html', context)
