document.querySelector("#form").addEventListener('submit', submitForm);

document.addEventListener("DOMContentLoaded", displayPost)

function submitForm(e) {
    e.preventDefault();
    
    //To get the value of the post
    postcontent = document.querySelector("#postContent").value;
    console.log(postcontent)

    //Sending the content to the server
    fetch('/newPost',{
        method: 'POST',
        body: JSON.stringify({
            content: postcontent
        })
    })
    .then(response => response.json())
    .catch(error => {
        console.log('Error', error);
    });

};

function displayPost(){
    
    fetch('/allPost')
    .then(response => response.json())
    .then(posts => {
        //console.log(posts);

        posts.forEach(function(post){
            const post_item = document.createElement('div')
            postContent = 
                `<div>
                    <p>${post.poster}</p>
                    <p>${post.content}</p>
                    <p>${post.dateTime}</p>
                    <p>${post.like}</p>
                </div>`
            
            post_item.innerHTML = postContent;
            document.querySelector('#posts').append(post_item);
        });
        
    });   
}