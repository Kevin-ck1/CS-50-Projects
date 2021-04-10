//Objects
//Contact Class:
class Contact {
    constructor(supplier, nameC, phone, email, position){
        this.supplier_id = supplier;
        this.name = nameC;
        this.pNumber = phone;
        this.email = email;
        this.position = position;
    }
};

class Product {
    constructor(category, supplierP, nameP, brand, price, size, weight, description){
        this.category = category;
        this.supplierP =  supplierP;
        this.nameP = nameP;
        this.brand = brand;
        this.price = price;
        this.size = size;
        this.weight = weight;
        this.description = description;
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
}


//UI Class
class UI {
    //Dislay the Contact
    static addContact(contact){
        const table = document.querySelector('.contact-table');

        const newRow = document.createElement('tr');
        
        newRow.innerHTML = `
            <tr>
                <th scope="row" class="rowCounter"></th>
                <td>${contact.name}</td>
                <td>${contact.pNumber}</td>
                <td>${contact.email}</td>
                <td>${contact.position}</td>
                <td class="text-center"><button class="btm btn-danger btn-sm delete-button">X</button></td>
            </tr>
        `;

        //Attaching the new row to the contact table
        table.insertBefore(newRow, table.firstChild)
    }

    static clearContactForm(){
        contactForm.querySelector('#supplier').value = '';
        contactForm.querySelector('#contact-name'). value = '';
        contactForm.querySelector('#contact-phone'). value = '';
        contactForm.querySelector('#contact-email'). value = '';
        contactForm.querySelector('#contact-position') . value = ''; 
    }

    //Remove Contact Entry
    static removeContact(tr){
        tr.remove();
    }

    //Giving the create row an id
    static renameRow(id1){
        const table = document.querySelector('.contact-table');
        table.firstChild.setAttribute('id', id1)
    }
    
}

//Storage
class Store {
    static storeContact(newContact){
        //Retrieving the csrftoken
        const csrftoken = (
            contactForm.querySelector('[name=csrfmiddlewaretoken]').value
        );
        const request = new Request(
            `/contactform`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request,{
            method: 'POST',
            mode: 'same-origin', 
            body: JSON.stringify({
                newContact: newContact
            })
        })
        .then(response => response.json())
        .then((res) =>{
            console.log(res.message)
            UI.renameRow(res.id)
        })
        
    };

    //Delete Contact
    static deleteContact(tr){
        //To get the crsf token
        const csrftoken = getCookie('csrftoken');

        const request = new Request(
            `/contactform`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request,{
            method: 'DELETE',
            mode: 'same-origin',
            body: `${tr.id}`
        })
        .then(response => response.json())
        .then((res) =>{
            console.log(res.message)
        })
    };
};

//Event Listener

//Add Contact
const contactForm = document.querySelector('#contact-form')
contactForm.addEventListener('submit', (event)=>{
    event.preventDefault();

    //Obtain the values from the form
    const supplier = contactForm.querySelector('#supplier').value;
    const nameC = contactForm.querySelector('#contact-name').value;
    const phone = contactForm.querySelector('#contact-phone').value;
    const email = contactForm.querySelector('#contact-email').value;
    const position = contactForm.querySelector('#contact-position') .value; 

    //Validating
    if(supplier === '' || nameC === '' || phone === '' || email === ''|| position === ''){
        alert("Please Fill in all the Fields");
    }else {
        //Creating a new contact from the data
        const newContact = new Contact(supplier, nameC, phone, email, position);
        
        //Adding the new contact to the UI for display
        UI.addContact(newContact);

        //Add to storage
        Store.storeContact(newContact);

        //Clear the fields
        UI.clearContactForm();
    }

});

//Delete Contact
document.querySelector('.contact-table').addEventListener('click',(event)=>{
    if (event.target.classList.contains('delete-button')){
        tr = event.target.parentElement.parentElement
        //Remove form display
        UI.removeContact(tr);

        //Remove from storage
        Store.deleteContact(tr);
    }
})