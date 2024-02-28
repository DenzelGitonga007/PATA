from django.shortcuts import render, redirect, HttpResponse
from . models import MissingPerson # posts models
from . forms import MissingPersonForm # form for uploading the missing person
from django.contrib import messages # to display the messages
from django.contrib.auth.decorators import login_required # to have users log in first


# Create your views here.
# Upload missing person's details
@login_required(login_url='accounts:login')
def create_missing_person(request):
    """Upload missing person's details"""

    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            missing_person = form.save(commit=False)
            missing_person.user = request.user
            
            missing_person.save()
            return HttpResponse('upload missing person success')
        else:
            messages.error(request, "Oops! Failed to upload missing person's details")

    else:
        form = MissingPersonForm()
    
    context = {'form': form}
    return render(request, 'posts/create_missing_person.html', context)
