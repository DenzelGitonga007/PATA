// Comments and show comments

$(document).ready(function () {
    // Attach click event handler to comment buttons
    $('.comment-btn').click(function (e) {
        e.preventDefault(); // Prevent default link behavior
        
        // Get the post ID from the button data attribute
        var postId = $(this).data('post-id');

        // Set the action attribute of the comment form to include the post ID
        // $('#comment-form').attr('action', '{% url "posts:comment_on_post" 0 %}'.replace('0', postId));
        $('#comment-form').attr('action', commentUrl.replace('0', postId));



        // Show the modal
        $('#commentModal').modal('show');
    });

    // Toggle comments visibility when "View all comments" link is clicked
    $('.toggle-comments-link').click(function (e) {
        e.preventDefault();
        var commentsId = $(this).data('toggle');
        $('#' + commentsId).toggle();
    });

    // Handle form submission for commenting
    $('#comment-form').submit(function (e) {
        e.preventDefault(); // Prevent default form submission
        
        // Serialize form data
        var formData = $(this).serialize();

        // Submit the form via AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function (response) {
                // Optionally, you can refresh the post details section to show the new comment
                // Close the modal
                $('#commentModal').modal('hide');
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});


// End of comments and show comments


// Reply to comment

$(document).ready(function () {
    // Attach click event handler to reply buttons
    $('.reply-btn').click(function (e) {
        e.preventDefault(); // Prevent default link behavior
        
        // Get the comment ID from the button data attribute
        var commentId = $(this).data('comment-id');

        // Set the comment ID in the hidden input field of the reply form
        $('#reply-form').find('.comment-id').val(commentId);

        // Show the modal for replying to comment
        $('#replyModal').modal('show');
    });

    // Handle form submission for replying to a comment
    $('#reply-form').submit(function (e) {
        e.preventDefault(); // Prevent default form submission
        
        // Serialize form data
        var formData = $(this).serialize();

        // Submit the form via AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function (response) {
                // Optionally, you can refresh the comments section to show the new reply
                // Close the modal for replying to comment
                $('#replyModal').modal('hide');
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});


// End of reply to comment


// Show Replies

$(document).ready(function () {
    // Attach click event handler to toggle-replies elements
    $('.toggle-replies').click(function () {
        // Toggle the visibility of replies container associated with the clicked comment
        $(this).siblings('.replies-container').toggle();
        // Change the text of the toggle-replies element to reflect its current state
        $(this).text(function (i, text) {
            return text === '▼ Show Replies' ? '▲ Hide Replies' : '▼ Show Replies';
        });
    });
});


// End of show replies