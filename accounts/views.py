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
# from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import io



# User creation
def user_creation_view(request):
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_email = form.cleaned_data.get('email')
            try:
                email_message = EmailMessage(
                    "Welcome to PATA",
                    "Lost a loved one? We would do our best in helping you find them. Upload their details, and you will be notified just as soon as anyone identifies them",
                    settings.EMAIL_HOST_USER,
                    [user_email],
                )
                email_message.send()
            except Exception as e:
                raise Exception("Email sending failed {}".format(str(e)))
            
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Oops! Something went wrong. Please correct the errors below.')

    else:
        form = CustomerUserCreationForm()
    
    context = {'form': form}
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
    
    # Filter posts of the user
    posts = user.missingperson_set.all()

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
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'accounts/profile.html', context)



# User profile report
@login_required(login_url='accounts:login')
def user_profile_report(request):
    # Get the currently logged-in user
    current_user = request.user

    # Count the number of posts associated with the logged-in user
    num_posts = MissingPerson.objects.filter(user=current_user).count()

    # Get the user's following and followers count
    user_profile = UserProfile.objects.get(user=current_user)
    num_following = user_profile.following.count()
    num_followers = user_profile.followers.count()

    # Prepare email content
    email_subject = 'Your Profile Report'
    email_body = (
        f"User Profile Report\n\n"
        f"Name: {current_user.username}\n"
        f"Posts: {num_posts}\n"
        f"Following: {num_following}\n"
        f"Followers: {num_followers}\n"
    )

    # Create and send the email
    email = EmailMessage(email_subject, email_body, to=[current_user.email])

    # Prepare CSV data
    csv_data = [
        ['Name', 'Posts', 'Following', 'Followers'],
        [current_user.username, num_posts, num_following, num_followers]
    ]

    # Create CSV file in memory
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerows(csv_data)

    # Attach the CSV file to the email
    email.attach('user_profile_report.csv', csv_buffer.getvalue(), 'text/csv')

    # Send the email
    email.send()

    # Return the CSV file as a downloadable response
    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_profile_report.csv"'
    return response


# FAQs
# @login_required(login_url='accounts/login')
def faqs(request):
    # Your logic to retrieve FAQ data from the database or any other source goes here
    # For now, let's assume you're passing an empty context
    context = {}
    return render(request, 'common/faqs.html', context)






# # User reports for admin if ever needed, but change the namings
# @login_required(login_url='accounts:login')
# def user_profile_report(request):
#     # Query all users and relevant information
#     users = CustomUser.objects.all()

#     # Prepare data for CSV export
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="user_profile_report.csv"'

#     # Create CSV writer
#     writer = csv.writer(response)
#     writer.writerow(['Username', 'Email', 'Date Joined', 'Number of Posts'])

#     # Write user data to CSV
#     for user in users:
#         # Count the number of posts associated with each user
#         num_posts = MissingPerson.objects.filter(user=user).count()
#         writer.writerow([user.username, user.email, user.date_joined, num_posts])

#     return response
