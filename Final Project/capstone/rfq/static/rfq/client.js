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
        console.log("Form fields cleared")
    }
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
            console.log(res.message)
        })
    }
};

//Event Listners
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