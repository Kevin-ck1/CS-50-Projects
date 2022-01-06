//Create Client Object
class Client {
    constructor (clientName, county, postal, number, email){
        this.clientName = clientName;
        this.county = county;
        this.postal = postal;
        this.clientNumber = number;
        this.emailClient = email;
    }
};

//Job object
class Job {
    constructor (client, items){
        this.client = client;
        this.itmes = items;
    }
};

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
};

//UI Class
class UI {
    //Display Client
    static displayClient(client){
        document.querySelector('#clientName').innerHTML = client.clientName;
        document.querySelector('#client-county').innerHTML = client.county;
        document.querySelector('#cNumber').innerHTML = client.clientNumber;
        document.querySelector('#cEmail').innerHTML = client.emailClient;
        document.querySelector('#cPostal').innerHTML = client.postal;
        console.log("Client Data Displayed Successfully")
    }
    //
    static resetForm(){
        document.querySelector('form').reset();
        console.log("Form fields cleared");
        document.querySelector('.form-client').style.display = 'none';
    };

    static displayClientList(clients){
        //console.log(clients)
        const ul = document.querySelector('#client-list')

        clients.forEach(element => {
            const li = document.createElement('li');
            li.setAttribute('class', 'list-group-item');
            li.style.display = 'none';
            li.innerHTML = element.clientName;
            ul.append(li);
        });

        //Creating a create client button if the client list is empty
        const createButton = document.createElement('li');
        createButton.setAttribute('class', 'list-group-item');
        createButton.setAttribute('id', 'createLink');
        createButton.innerHTML = `
            <p>
            Client Does don't Exist. 
            <span class="link">Click Here to create Client</span>
            </p>
        `


    };
};

//Store Class

class Store {
    static storeClient(client){
        //Get Crsf token
        const csrftoken = (
            document.querySelector('#clientForm')
            .querySelector('[name=csrfmiddlewaretoken]').value
        );
        const request = new Request(
            `/clients`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request, {
            method: "POST",
            mode: 'same-origin', 
            body: JSON.stringify({
                newClient : client
            })
        })
        .then(response => response.json())
        .then(res => {
            console.log(res.message);
            console.log(res.id);
        })
    };

    
    static getClients(){
        var clients;
        fetch("/clients")
        .then(response => response.json())
        .then(res => {
            //Display items in list of clients
            UI.displayClientList(res)
        })
    }

};

//Search Class

class SearchClient{
    static clientFilter(){
        const clientFilterValue = clientSearch.value.toUpperCase();
        console.log(clientFilterValue);
        const clientItem = document.querySelectorAll('.list-group-item');
        clientItem.forEach(client => {
            if(client.innerHTML.toUpperCase().indexOf(clientFilterValue) > -1 && clientFilterValue.length > 0 ){
                client.style.display = '';
            }else{
                client.style.display = 'none';
            };
        });
    }
}

//Event Listners

//Load Clients
document.addEventListener('DOMContentLoaded', ()=>{
    //Get list of clients
    Store.getClients();
});

//Display Creat client form
document.querySelector('#createClient').querySelector('button').addEventListener('click', ()=>{
    document.querySelector('.form-client').style.display = '';
})

//Submit Form
document.querySelector('#clientForm').addEventListener('submit', (event)=>{
    event.preventDefault()
    console.log('Form submit button clicked')
    //Obtaining the form data
    const data = new FormData(document.querySelector('#clientForm'));
    const clientName = data.get("client-name");
    const county = data.get("county");
    const postal = data.get("postal-address");
    const clientNumber = data.get("phone-number");
    const emailClient = data.get("email-address");

    if (clientName === '' || county === '' || postal === '' || clientNumber === '' || emailClient === '' ){
        alert('Please Fill in all fields')
    } else{
        const newClient = new Client (clientName, county, postal, clientNumber, emailClient,)
        console.log(newClient)
        //Display Clients Details
        UI.displayClient(newClient);

        //Clear Form Fields
        UI.resetForm();
        //Store Clients Details in database
        Store.storeClient(newClient);

    };    
});

//Search bar
const clientSearch = document.querySelector('#search-client')
clientSearch.addEventListener('keyup', SearchClient.clientFilter)
