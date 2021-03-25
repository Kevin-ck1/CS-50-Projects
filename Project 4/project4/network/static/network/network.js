document.addEventListener('DOMContentLoaded', function(){
    //Event Listener for submiting the form
    document.querySelector("#form").addEventListener('submit', submitForm);

    //Event Listener for clicking the followning link
    document.querySelector('#followingLink').addEventListener('click', () =>{
        document.querySelector('#create').style.display = "none";
        document.querySelector('#profile').style.display ="none";
    });

    //To obtain a person who has post a particular post
    var postname = document.querySelector('#posterUsername').dataset.idno;
    //Event Listener for clicking a post poster
    document.querySelectorAll("#posterUsername").forEach((a) => {
        a.addEventListener('click', () => viewProfile(postname));
    });

    //To obtain the post id
    //var postId = document.querySelector('#postContent').dataset.postId;
    
    //var postid = document.querySelector('#editButton').dataset.postId;
    
    //Event Listener for Editing Post
    document.querySelectorAll('#editButton').forEach((link) => {
        //console.log(postid)
        //link.addEventListener('click', ()=> editPost(postid))

    });

    let currentuser2 = document.querySelector('#currentUser1').dataset.currentUser;
    console.log(currentuser2)

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
        var profileId = document.querySelector('#followbutton').dataset.idno
        document.querySelector('#followbutton').addEventListener('click', () => followUnfollow(profileId));

    });
};

function followUnfollow(p){
    fetch(`/followUnfollow/${p}`)
    .then(response => response.json())
    .then(a => {
        document.querySelector('#followNo').innerHTML = a.followers
        document.querySelector('#followbutton').innerHTML = a.buttontype
    });
};

function editPost(id){
    // fetch(`/editPost/${id}`, {
    //     method: 'POST',
    //     body: JSON.stringify({
    //         content: postcontent
    //     })
    // });
    console.log(id)
};

function likes(o){
    fetch(`/likePost/${0}`)
}