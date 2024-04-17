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
            # Create UserProfile for the new user
            # UserProfile.objects.create(user=user)
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


# User profile
@login_required(login_url='accounts:login')
def user_profile(request, username):
    """Display user profile"""
    user = get_object_or_404(CustomUser, username=username)
    profile = get_object_or_404(UserProfile, user=user)

    # Check if the current user is already following the user
    is_following = profile.followers.filter(username=request.user.username).exists()

    # Get the counts of followers and following
    followers_count = profile.followers.count()
    following_count = profile.following.count()

    if request.method == 'POST':
        if 'follow' in request.POST:
            if not is_following:
                # Add the current user to the followers of the profile user
                profile.followers.add(request.user)
                # Increase the following count of the current user
                request.user.userprofile.following.add(profile.user)
                # Redirect back to the profile
                return redirect('accounts:user_profile', username=username)
        elif 'unfollow' in request.POST:
            if is_following:
                # Remove the current user from the followers of the profile user
                profile.followers.remove(request.user)
                # Decrease the following count of the current user
                request.user.userprofile.following.remove(profile.user)
                # Redirect back to the profile
                return redirect('accounts:user_profile', username=username)

    context = {
        'user': user,
        'profile': profile,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'accounts/profile.html', context)
