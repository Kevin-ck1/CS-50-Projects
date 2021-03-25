document.querySelector("#form").addEventListener('submit', submitForm);

//cument.addEventListener("DOMContentLoaded", displayPost)
var postname = document.querySelector('#posterUsername').dataset.idno;

document.querySelectorAll("#posterUsername").forEach((a) => {
    a.addEventListener('click', () => viewProfile(postname))
});

document.querySelector('#followingLink').addEventListener('click', () =>{
    document.querySelector('#create').style.display = "none";
    document.querySelector('#profile').style.display ="none";
});

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
    document.querySelector('#display_posts').style.display ="none"
    fetch('/allPost')
    .then(response => response.json())
    .then(posts => {
        //console.log(posts);

        posts.forEach(function(post){
            const post_item = document.createElement('div')
            postContent = 
                `<div class="border">
                    <p id="posterUsername">${post.poster}</p>
                    <p>${post.content}</p>
                    <p>${post.dateTime}</p>
                    <p>${post.like}</p>
                </div>`
            
            post_item.innerHTML = postContent;
            document.querySelector('#posts').append(post_item);
            document.querySelector("#posterUsername").addEventListener('click',() => viewProfile(post.poster))
        });
        
    });   
}

function viewProfile(p){
    //document.querySelector('body').animate({ scrollTop: 0 }, "slow");
    fetch(`/profile/${p}`)
    .then( response => response.text())
    .then( html => {
        document.body.innerHTML = html;
        window.scrollTo(0, 0);
        document.querySelector('#create').style.display = "none"

    })
}
