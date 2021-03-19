document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //My added events
  // To initiate post request, when posting the mail
  document.querySelector('#compose-form').addEventListener('submit', post_email);
  //To view an email
  //document.querySelector('#mail').addEventListener('click', () => view_mail(`${email.id}`));
  //document.querySelectorAll('#mail').forEach(email_item =>{
  //   email_item.onclick = function() {
  //       view_mail(this.dataset.emailNo);
  //   }
//})
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //My code
  //Fetching the sent mail
  fetch('/emails/'+mailbox+'')
  //fetch(`/emails/${mailbox}`) -- This can also be used for the fetch url
    .then(response => response.json())
    .then(emails => {
        // Print emails
        //console.log(emails);
        let email_list = "";
        emails.forEach(function(email) {
          email_list += 
          // <div id="email${email.id}" class="card card-body">
          //   <p> 
          //     <span class="col-3" >${email.sender}</span>
          //     <span>${email.subject}</span>
          //     <span class="text-muted">${email.timestamp}</span>
          //   </p>
          // </div>`;
          `
          <div id="email" class="card card-body" data-emailNo=${email.id}>
            <p> 
              <span class="col-3" >${email.sender}</span>
              <span>${email.subject}</span>
              <span class="text-muted">${email.timestamp}</span>
            </p>
          </div>`;

          
          //console.log(email)
         // document.querySelector(`#mail${email.id}`).addEventListener('click', () => view_mail(`${email.id}`));
        });

        const element = document.createElement('div');
        element.innerHTML = email_list;
        document.querySelector('#emails-view').append(element)
        // ... do something else with emails ...

        const check_mail =  document.createElement('div');
        check_mail.setAttribute("id", "mail");
        check_mail.setAttribute("class", "card card-body");
        check_mail.addEventListener('click', () => view_mail(`${email.id}`));
        check_mail.innerHTML = email_list
        document.querySelector('#emails-view').append(check_mail)




});


}

//My Functions
function post_email(e) {
  e.preventDefault();
  
  const compose_recipients = document.querySelector('#compose-recipients').value;
  const compose_subject = document.querySelector('#compose-subject').value;
  const compose_body = document.querySelector('#compose-body').value;
  console.log(compose_subject)

  fetch('/emails', {

    method: 'POST',
    body: JSON.stringify({
        recipients: compose_recipients,
        subject: compose_subject,
        body: compose_body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  })

  .catch(error => {
    console.log('Error', error);
  });

  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));

  
}

function view_mail(emailNo){
  fetch(`/emails/${emailNo}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // ... do something else with email ...
});

}