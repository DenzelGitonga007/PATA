document.addEventListener("DOMContentLoaded", function() {
    const likeBtns = document.querySelectorAll(".like-btn");

    likeBtns.forEach(likeBtn => {
        likeBtn.addEventListener("click", function() {
            const postId = likeBtn.dataset.postId;

            fetch(`/posts/react/${postId}/`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken, // Use the CSRF token variable here
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                // Update the like count dynamically
                const likeCountElement = likeBtn.nextElementSibling;
                likeCountElement.innerText = data.likeCount;
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    });
});


// Commenting

// End of commenting