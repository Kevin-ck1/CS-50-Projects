document.addEventListener('DOMContentLoaded', function(){
    //Obtain current User
    // let currentUser = document.querySelector('#currentUser').dataset.currentuser;
    // console.log(currentUser);

    //Display Post
    displayPost();

    //Event Listener for submiting the form
    document.querySelector("#form").addEventListener('submit', submitForm);

    //Event Listener for clicking the followning link
    document.querySelector('#followingLink').addEventListener('click', () =>{
        document.querySelector('#create').style.display = "none";
        document.querySelector('#profile').style.display ="none";
    });

    //To obtain a person who has post a particular post
    let postname = document.querySelector('#posterUsername').dataset.idno;
    //Event Listener for clicking a post poster
    document.querySelectorAll("#posterUsername").forEach((a) => {
        a.addEventListener('click', () => viewProfile(postname));
    });

    //To obtain the post id
   
    document.querySelectorAll('#editButton').forEach((link) => {
       
        let postId = document.querySelector('#editButton').dataset.postid;
        link.addEventListener('click', ()=> console.log(postId))

    });

    // let currentuser2 = document.querySelector('#currentUser1').dataset.currentuser;
    // console.log(currentuser2)

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

function displayPost(a){
    document.querySelector('#display_posts').style.display ="none"
    document.querySelector('#posts').innerHTML = ""
    fetch(`/allPost?page=${a}`)
    .then(response => response.json())
    .then(posts => {
        //Iterating to get a list of diplayed posts
        console.log()
        posts.forEach(function(post){
            const post_item = document.createElement('div')
            //Getting the current User
            let currentUser = document.querySelector('#currentUser').dataset.currentuser;

            //Logic for handling the display button
            if(currentUser =! post.poster){
                editbutton = `<p class="link mr-3" id="editButton">Edit</p>`
            }else{
                editbutton = ``
            };

            postContent = 
               ` <div class="card mt-2" id="postContent">
                    <div class="card-header">
                        <h3 class="media-heading">
                            <span id="posterUsername">${post.poster}</span>
                            <small><i>${post.dateTime}</i></small>
                        </h3>
                    </div>
                    <div class="card-body">
                        <p>${post.content}</p>
                        <div class="row justify-content-between">
                            <p class="text-muted ml-3">Likes ${post.like}</p>
                            ${editbutton}
                        </div>
                    </div>
                </div>`;
            
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