from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomerUserCreationForm # custom user creation forms
from .models import CustomUser
from django.contrib import messages
from django.core.mail import send_mail # to send the mail after successful email creation

# Create your views here.
# User creation
def UserCreationView(request):
    """Creates the user account"""
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST) # initialize the form
        if form.is_valid():
            form.save()
            # Successful creation
            # send the email
            messages.success(request, 'Account created successful. You can now log in with your details')
            # return redirect('accounts:login') # take back to login page
            return HttpResponse('Registration successfull')
        else:
            messages.error(request, 'Oops! Something went wrong. Try again later')
    else:
        form = CustomerUserCreationForm()
    
    # The template
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


