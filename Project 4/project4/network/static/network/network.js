document.addEventListener('DOMContentLoaded', function(){
    //To obtain the current user
    let currentUser = document.querySelector('#currentUser1').dataset.currentuser;
    //console.log(currentUser);

    try{
        //Event Listener for submiting the form
        document.querySelector("#form").addEventListener('submit', submitForm);
            //event.preventDefault();
            
    }
    catch{
        console.log("Visit All_Posts Page to Make a post, :)")
    }
});

try{
    //To obtain a person who has post a particular post
    let postname = document.querySelector('#posterUsername').dataset.idno;
    //Event Listener for clicking a post poster
    document.querySelectorAll("#posterUsername").forEach((a) => {
        a.addEventListener('click', () => {
            history.pushState({state:postname},"",`/profile/${postname}`);
            viewProfile(postname);
        });
    });
}
catch{
    console.log("No Posts Yet, Watch Snyder's Cut While Waiting :)")
}


//Function for getting crsf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submitForm(e) {
    e.preventDefault()
    //To get the csrftoken
    const csrftoken = (
        document.querySelector('#form')
        .querySelector('[name=csrfmiddlewaretoken]').value
    );
    console.log(csrftoken)
    const request = new Request(
        `/newPost`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    
    //To get the value of the post
    let postcontent = document.querySelector("#postContent").value;
    console.log(postcontent)

    //Sending the content to the server
    fetch(request,{
        method: 'POST',
        mode: 'same-origin', 
        body: JSON.stringify({
            content: postcontent
        })
    })
    .then(response => response.json())
    .then(document.querySelector("#postContent").innerHTML="")
    .then(()=>{
        location.reload();
    })
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
    fetch(`/profile/${p}`)
    .then( response => response.text())
    .then( html => {
        document.body.innerHTML = html;
        window.scrollTo(0, 0);
        try{
            var profileId = document.querySelector('#followbutton').dataset.idno
            document.querySelector('#followbutton').addEventListener('click', () => followUnfollow(profileId));
        }
        catch{
            console.log("Hear me, and rejoice! This is your Profile")
        }

    });
};

function followUnfollow(p){
    fetch(`/followUnfollow/${p}`)
    .then(response => response.json())
    .then(a => {
        document.querySelector('#followNo').innerHTML = a.followers;
        document.querySelector('#followbutton').innerHTML = a.buttontype;
    });
};

function editPost(id){
    originalText = document.querySelector(`#post${id}`).querySelector('#postcontent').innerHTML;
    document.querySelector(`#post${id}`).querySelector('#postbody').style.display="none"
    editForm = document.createElement('div')
    editForm.setAttribute("id", "editForm");
    form = 
        `<div id="editing" >
            <div class="card-header">
                <h3>Editing Post</h3>
            </div>
            <div class="card-body" id="post_form">
                <textarea name="postArea" id="editContent" cols="10" rows="2" class="form-control">${originalText}</textarea>
                <button id="updateButton" class="btn btn-primary mt-2" onclick="updatepost(${id})">Update</button>
            </div>
        </div>`
    //<input class="btn btn-primary mt-2" type="submit" value="Update">
    editForm.innerHTML = form;
    document.querySelector(`#post${id}`).append(editForm); 
};

function updatepost(id){
    //To get the crsf token
    const csrftoken = getCookie('csrftoken');
    console.log(csrftoken);

    const request = new Request(
        `/updatePost/${id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    editedcontent = document.querySelector("#editContent").value;
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin', 
        body: JSON.stringify({
            content: editedcontent
        })
    })
    .then(response => response.json())
    .then((res) => {
        console.log(res.message)
        document.querySelector(`#post${id}`).querySelector('#postbody').style.display="contents";
        document.querySelector(`#post${id}`).querySelector('#postcontent').innerHTML = editedcontent;
        document.querySelector(`#post${id}`).querySelector('#editForm').remove()
    });
};


function likepost(id){
    fetch(`/likePost/${id}`)
    .then(response => response.json())
    .then(a => {
        if(a.like){
            document.querySelector(`#post${id}`).querySelector('#heartIcon').innerHTML=`&#x2661;`;
            document.querySelector(`#post${id}`).querySelector('#heartIcon').removeAttribute("class");
            document.querySelector(`#post${id}`).querySelector('#likeno').removeAttribute("class");  
        }else{
            document.querySelector(`#post${id}`).querySelector('#heartIcon').innerHTML=`&#x2665;`;
            document.querySelector(`#post${id}`).querySelector('#heartIcon').setAttribute("class", "red");
            document.querySelector(`#post${id}`).querySelector('#likeno').setAttribute("class", "red");
        };
        document.querySelector(`#post${id}`).querySelector('#likeno').innerHTML = a.likes;
        
    });
}

function showcomments(id){
    fetch(`/displayComments/${id}`)
    .then(response => response.text())
    .then( html =>{
        document.querySelector(`#post${id}`).querySelector('.commentslists').innerHTML=html
        let commentForm = document.querySelector(`#post${id}`).querySelector('.commentform')
        commentForm.addEventListener('submit', function(event){  
            event.preventDefault()
            createComment(id)
        });
    })
    .catch(error => {
        console.log('Error', error);
    });
};

function createComment(id){
    let commentContent = document.querySelector(`#post${id}`).querySelector('#commentContent').value;
    const csrftoken = (
        document.querySelector(`#post${id}`)
        .querySelector('.commentform')
        .querySelector('[name=csrfmiddlewaretoken]').value
    );
    const request = new Request(
        `/createComment/${id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    
    fetch(request,{
        method: 'POST',
        mode: 'same-origin', 
        body: JSON.stringify({
            content: commentContent
        })
    })
    .then(commentContent.value="")
    .then(response => response.text())
    .then( html =>{
        document.querySelector(`#post${id}`).querySelector('.commentslists').innerHTML=html
    })
    .catch(error => {
        console.log('Error', error);
    });
}
