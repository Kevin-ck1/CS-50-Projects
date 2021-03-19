document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  

  //My added events
  // To initiate post request, when posting the mail
  document.querySelector('#compose-form').addEventListener('submit', post_email);
  

  // By default, load the inbox
  load_mailbox('inbox');
});


var state;

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  try {
    document.querySelector('#readMail').remove();
  }
  catch{}

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  //Fetching sent mail
  fetch('/emails/'+mailbox+'')
  //fetch(`/emails/${mailbox}`) -- This can also be used for the fetch url
    .then(response => response.json())
    .then(emails => { 

      //Displaying the emails in a table format
      const emailTable =  document.createElement('div');
      emailTable.setAttribute("id", "mail");
      emailTable.setAttribute("class", "col-12");
      const tableBody = document.createElement('div');
      tableBody.setAttribute("id", "tableBody")
      emailTable.append(tableBody)

      //Iterating the emails and placing each into a row
        let email_list = "";
        emails.forEach(function(email) {
          if (state == "sent"){
            email_list = 
            ` <div class="col-3">To: ${email.recipients}</div>
              <div>${email.subject}</div>
              <div class="ml-auto">${email.timestamp}</div>
            `;
          }else{
            email_list = 
          ` <div class="col-3">${email.sender}</div>
            <div>${email.subject}</div>
            <div class="ml-auto">${email.timestamp}</div>
          `;
          };
          
          emailRow = document.createElement('div');
          emailRow.innerHTML = email_list;
          emailRow.setAttribute("class", "d-flex border-bottom border-dark p-2")
          emailRow.setAttribute("id", "emailRow")

          //To show read status of the email
          if(email.read){
            emailRow.style.backgroundColor = "#f1f1f1"
          };
          //To view the mail once clicked
          emailRow.addEventListener("click", ()=>view_mail(email.id));
          tableBody.append(emailRow);    
        }); 
        //Appending the table to the view div
        document.querySelector('#emails-view').append(emailTable);     

    });

  state = mailbox
  //console.log(state)

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  try {
    document.querySelector('#readMail').remove();
  }
  catch{}

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

}

//To post an email
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
  .catch(error => {
    console.log('Error', error);
  });

  fetch(`/emails/sent`)
  load_mailbox('sent')
}

function view_mail(emailNo){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  const read_mail =  document.createElement('div');
  read_mail.setAttribute("id", "readMail");
  read_mail.style.display = 'flex';
  document.querySelector('.container').append(read_mail);
  

  fetch(`/emails/${emailNo}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      
      read_mail.innerHTML = `
      <div class="col-12">
        <div class="row justify-content-between">
        <h2 class="pl-2">${email.subject}</h2>
        <input type="button" id="button1">
        </div>
        <hr>
        <div class="row justify-content-between">
          <div>
          <span class="font-weight-bold pl-4"> ${email.sender}</span>
          to
          <span class"text-muted">${email.recipients}</span>
          </div>
          <div >
          <span class"text-muted">${email.timestamp}</span>
          </div>
        </div>
        <hr>
        <p class="pl-2" style="white-space: pre-line">${email.body}</p>
        <div class="">
          <button class="btn btn-sm btn-primary" id="reply">Reply</button>
        </div>
      </div>
      
      `
     button1 = document.querySelector('#button1')
      if (state == "inbox"){
        button1.setAttribute("value", "Archive");
        button1.setAttribute("class", "btn btn-sm btn-info")
      }else if (state == "archive"){
        button1.value = "Unarchive"
        button1.setAttribute("class", "btn btn-sm btn-warning")
      }else {
        button1.style.display = "none"
      }

      button1.addEventListener('click', () => archiveState(email.id));
      document.querySelector('#reply').addEventListener('click', () => replyMail(email.id));
  });

  fetch(`/emails/${emailNo}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archiveState(emailNo){
  var status; 

  if (state == "inbox"){
    status = true
  }else {
    status = false
  }

  fetch(`/emails/${emailNo}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: status
    })
  });

  load_mailbox('inbox');
}

function replyMail(emailNo){
  fetch(`/emails/${emailNo}`)
  .then(response => response.json())
  .then(email =>{
    compose_email()
    var email_subject;
    var a = email.subject
    if(a.includes("RE:")){
      email_subject = a
    }else{
      email_subject = `RE: ${a}`
    }
    if(state == "sent"){
      document.querySelector('#compose-recipients').value = email.recipients;
    }else{
      document.querySelector('#compose-recipients').value = email.sender;
    }
    document.querySelector('#compose-subject').value = email_subject;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \r\n [${email.body}]: \r\n`
  });
}

