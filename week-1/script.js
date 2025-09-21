const API_URL = 'https://jsonplaceholder.typicode.com/posts';

// Part 1: Fetching posts
document.getElementById('fetch-posts-btn').addEventListener('click', () => {
    fetch(API_URL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(posts => {
            const postsContainer = document.getElementById('posts-container');
            postsContainer.innerHTML = ''; // Clear previous posts
            posts.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h4>${post.title}</h4>
                    <p>${post.body}</p>
                `;
                postsContainer.appendChild(postDiv);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('Failed to fetch posts. Check the console for more details.');
        });
});

// Part 2: Creating a new post
document.getElementById('create-post-form').addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent the form from submitting normally

    const title = document.getElementById('post-title').value;
    const body = document.getElementById('post-body').value;

    const newPost = {
        title: title,
        body: body,
        userId: 1
    };

    fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newPost)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to create post');
        }
        return response.json();
    })
    .then(data => {
        alert('Post created successfully! ID: ' + data.id);
        console.log('New Post Created:', data);
    })
    .catch(error => {
        console.error('Error creating post:', error);
        alert('Failed to create post. Check the console for more details.');
    });
});