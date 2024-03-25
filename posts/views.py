from django.shortcuts import render, redirect
from .models import MissingPerson
from .forms import MissingPersonForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required(login_url='accounts:login')
def create_missing_person(request):
    """Upload missing person's details"""
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            missing_person = form.save(commit=False)
            missing_person.user = request.user
            missing_person.save()
            messages.success(request, 'Your post is now live! We hope you find the person soon')
            return redirect('posts:posts_index')  # Add return statement here
        else:
            messages.error(request, "Oops! Failed to upload missing person's details")
    else:
        form = MissingPersonForm()
    context = {'form': form}
    return render(request, 'posts/create_missing_person.html', context)




@login_required(login_url='accounts:login')
def posts_index(request):
    """
    Fetch or display all posts
    """
    posts = MissingPerson.objects.all().order_by('-created_at')
    # If the user has just posted, their post should appear first
    if request.user.is_authenticated:
        user_posts = posts.filter(user=request.user)
        if user_posts.exists():
            user_post = user_posts.first()
            other_posts = posts.exclude(pk=user_post.pk)
            posts = [user_post] + list(other_posts)
    context = {'posts': posts}
    return render(request, 'posts/posts_index.html', context)
