$(document).ready(function() {
    $('.like-btn').click(function() {
        const likeBtn = $(this); // Store a reference to the like button
        const newsId = likeBtn.data('id');
        const action = 'like';
        const url = likeBtn.data('url');

        // Update the like count immediately by adding 1
        const likeCountElement = $('#likes-count-' + newsId);
        likeCountElement.text(parseInt(likeCountElement.text()) + 1);

        likeDislikeNews(newsId, action, url);
    });

    $('.dislike-btn').click(function() {
        const dislikeBtn = $(this); // Store a reference to the dislike button
        const newsId = dislikeBtn.data('id');
        const action = 'dislike';
        const url = dislikeBtn.data('url');

        // Update the dislike count immediately by adding 1
        const dislikeCountElement = $('#dislikes-count-' + newsId);
        dislikeCountElement.text(parseInt(dislikeCountElement.text()) + 1);

        likeDislikeNews(newsId, action, url);
    });

    function likeDislikeNews(newsId, action, url) {
        // Get CSRF token from cookies
        const csrftoken = getCookie('csrftoken');

        // Include CSRF token in request headers
        $.ajax({
            url: url,
            method: 'POST',
            headers: { "X-CSRFToken": csrftoken },
            data: { id: newsId, action: action },
            success: function(response) {
                // Update like/dislike count on the page with the response
                $('#likes-count-' + newsId).text(response.likes);
                $('#dislikes-count-' + newsId).text(response.dislikes);
            },
            error: function(xhr, status, error) {
                console.error(error);
                // Revert the like/dislike count if there's an error
                if (action === 'like') {
                    $('#likes-count-' + newsId).text(parseInt($('#likes-count-' + newsId).text()) - 1);
                } else if (action === 'dislike') {
                    $('#dislikes-count-' + newsId).text(parseInt($('#dislikes-count-' + newsId).text()) - 1);
                }
            }
        });
    }

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
