//Supplier Class
class Supplier{
    constructor(nameS, address, email, contact, zone, location){
        this.nameS = nameS;
        this.address = address;
        this.email = email;
        this.contact = contact;
        this.zone = zone;
        this.location = location;
    }
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

function requestPath(url){
    //Get csrf token
    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        `${url}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    return request;
}

//UI Class: User Interface
class UI {
    static clearForm(){
        document.querySelector('#nameS').value = '';
        document.querySelector('#address').value = '';
        document.querySelector('#email').value = '';
        document.querySelector('#contact').value = '';
        document.querySelector('#zone').value = '';
        document.querySelector('#nameS').value = '';
    }

    static supplierDetails(id){
        window.location=`/company/suppliers/${id}`
    }
}

//Storage Class
class Storage {
    static addSupplier(supplier){
        const request = requestPath(`supplierform`);
        console.log(request)
        fetch(request, {
            method: "POST",
            mode: "same-origin",
            body: JSON.stringify({
                newSupplier: supplier
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
            window.location=`/company/suppliers/${res.id}`
              
        })
        
    }
}

//Events
try {
    //Clicking Product: Opening supplier details
    document.querySelector('#supplierTable').querySelectorAll('tr').forEach((tr)=>{
        tr.addEventListener('click', ()=>{
            UI.supplierDetails(tr.id)
        })
    })
} catch {
    //Submiting Form
    document.querySelector('#supplierForm').addEventListener('submit', (e)=>{
        e.preventDefault();
        const nameS = document.querySelector('#nameS').value;
        const address = document.querySelector('#address').value;
        const email = document.querySelector('#email').value;
        const contact = document.querySelector('#contact').value;
        const zone = document.querySelector('#zone').value;
        const location = document.querySelector('#nameS').value;

        if(nameS == '' || address == '' || email =='' || contact == '' || zone == '' || location == ''){
            alert('Please Fill in All the Fields')
        }else{
            const newSupplier = new Supplier(nameS, address, email, contact, zone, location)

            //Add The new Supplier to the database
            Storage.addSupplier(newSupplier);

            //Clear Form Fields
            UI.clearForm()
        }

    })
}

