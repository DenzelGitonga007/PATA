from django.shortcuts import get_object_or_404, render, redirect
from .models import MissingPerson, Comment
from .forms import CommentReplyForm, MissingPersonForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse



"""
CRUD FOR THE POSTS:

Create - Create/post missing person's details
Read 1 - Read/view details of the missing person, both for the user who posted, and everyone else in the world
Read 2 - Read/view details of the missing person, both for the user who posted, and everyone else in the world: only viewing
Update - User who posted, is able to update the details of the missing person
Delete - User who posted is able to delete the missing person

"""


# Create
@login_required(login_url='accounts:login')
def create_missing_person(request):
    """Upload missing person's details"""
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            missing_person = form.save(commit=False)
            missing_person.user = request.user
            missing_person.save()
            user_email = request.user.email # get the email of the logged in user who posted
            # Send email upon successful posting
            try:
                email_message = EmailMessage(
                    "Post submitted successfully", #subject
                    "The missing person's details are now live. We hope you find them soon", # message
                    settings.EMAIL_HOST_USER, # sender's email
                    [user_email], # recepient email
                )
                email_message.send()
            except Exception as e:
                raise Exception("Email sending failed {}".format(str(e)))
            # End of email send


            messages.success(request, 'Your post is now live! We hope you find the person soon')
            return redirect('posts:posts_index')
        else:
            messages.error(request, "Oops! Failed to upload missing person's details")
    else:
        form = MissingPersonForm()
    context = {'form': form}
    return render(request, 'posts/create_missing_person.html', context)

# Read 1-- Display all posts
@login_required(login_url='accounts:login')
def posts_index(request):
    """
    Fetch and display all posts
    """
    posts = MissingPerson.objects.all().order_by('-created_at')
    # If the user has just posted, their post should appear first
    if request.user.is_authenticated:
        user_posts = posts.filter(user=request.user)
        if user_posts.exists():
            user_post = user_posts.first()
            other_posts = posts.exclude(pk=user_post.pk)
            posts = [user_post] + list(other_posts)
    
    # Fetch comments and reactions for each post
    post_data = []
    for post in posts:
        comments = post.comment_set.all()  # Retrieve comments for each post
        # reactions = post.reaction_set.all()  # Retrieve reactions for each post
        post_data.append({
            'post': post,
            'comments': comments,
            # 'reactions': reactions,
        })
    
    context = {'post_data': post_data}
    return render(request, 'posts/posts_index.html', context)



# Read 2 -- viewing the details: only viewing
@login_required(login_url='accounts:login')
def view_post_details(request, post_id):
    """
    View the particular post details
    """
    post = get_object_or_404(MissingPerson, pk=post_id)
    comments = post.comment_set.all()  # Retrieve comments for the post
    # reactions = post.reaction_set.all()  # Retrieve reactions for the post
    
    context = {
        'post': post,
        'comments': comments,
        
    }
    return render(request, 'posts/view_post_details.html', context)


# Update
@login_required(login_url='accounts:login')
def update_post(request, post_id):
    """
    Update the details of the post

    """
    post = get_object_or_404(MissingPerson, pk=post_id)
    # Check if the current user is the owner of the post
    if post.user != request.user:
        messages.error(request, "You don't have permission to update this post.")
        return redirect('posts:posts_index')
    
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('posts:posts_index')
        else:
            messages.error(request, 'Failed to update the post')
    else:
        form = MissingPersonForm(instance=post)
    context = {'form': form}
    return render(request, 'posts/update_post.html', context)


# Delete
@login_required(login_url='accounts:login')
def delete_post(request, post_id):
    """
    Delete the post

    """
    post = get_object_or_404(MissingPerson, pk=post_id)
    # Check if the user deleting is the one who posted
    if post.user != request.user:
        messages.error(request, "You don't have permission to delete this post")
        return redirect('posts:posts_index')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted successfully!')
        return redirect('posts:posts_index')



# Comment
@login_required(login_url='accounts/login')
def comment_on_post(request, post_id):
    post = get_object_or_404(MissingPerson, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            # Notify the post owner
            messages.info(request, f'New comment on your post by {request.user.username}')
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            # Return a JSON response with form errors if the form is not valid
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        # Return a JSON response with an error if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=405)



# Reply to comment
@login_required(login_url='accounts/login')
def reply_to_comment(request, comment_id):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment  # Assign the parent comment
            reply.save()
            messages.info(request, f'New reply to your comment by {request.user.username}')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




# Liking a post
@login_required(login_url='accounts:login')
def react_to_post(request, post_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        post = get_object_or_404(MissingPerson, pk=post_id)
        
        # Toggle like for the current user
        post.toggle_like(request.user)
        
        # Save the post instance to persist changes to the database
        post.save()
        
        # Get the updated like count for the post
        like_count = post.liked_by.count()
        
        # Return JSON response with the updated like count
        return JsonResponse({'likeCount': like_count})
    else:
        # Handle invalid request method or non-ajax request
        return JsonResponse({'error': 'Invalid request'}, status=400)

