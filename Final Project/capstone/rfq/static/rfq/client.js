//Create Client Object
class Client {
    constructor (name, county, postal, number, email){
        this.clientName = name;
        this.county = county;
        this.postal = postal;
        this.clientName = name;
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
    static addClient(){

    }
};

//Store Class

class Store {

};

//Event Listners
document.querySelector('#clientForm').addEventListener('submit', (event)=>{
    event.preventDefault()
    console.log('Form submited-Line 45')
    

})