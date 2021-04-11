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
        this.supplierP_id =  supplierP;
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
    
    //Display Contact Form
    static displayContactForm(){
        document.querySelector('.addContact').style.display = 'none';
        document.querySelector('.addingContacts').style.display = '';
    };

    //Hide Contact Form
    static hideContactForm(){
        document.querySelector('.addContact').style.display = '';
        document.querySelector('.addingContacts').style.display = 'none';
    };

    //Display Product Form
    static displayProductForm(){
        document.querySelector('.addProduct').style.display = 'none';
        document.querySelector('.productForm').style.display='';
    };

    //Hide Product Form
    static hideProductForm(){
        document.querySelector('.addProduct').style.display = '';
        document.querySelector('.productForm').style.display='none'; 
    }


    //Add the Contact
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
    static removeRow(tr){
        tr.remove();
    }

    //Giving the create row an id
    static renameRow(id1){
        const table = document.querySelector('.contact-table');
        table.firstChild.setAttribute('id', id1)
    }

    //Add Product
    static addProduct(product){
        const table = document.querySelector('.product-table')

        const newRow = document.createElement('tr')
        newRow.innerHTML = `
        <tr>
            <th scope="row" class="rowCounter"></th>
            <td>${product.category}</td>
            <td>${product.nameP}</td>
            <td>${product.brand}</td>
            <td>${product.description}</td>
            <td>${product.price}</td>
            <td class="text-center"><button class="btm btn-danger btn-sm delete-product">X</button></td>
            <td class="text-center" hidden><button class="btm btn-success btn-sm">Add</button></td>
        </tr>
        `
        //Attaching the new row to the contact table
        table.insertBefore(newRow, table.firstChild);
    };

    //Clear Product Form
    static clearProductForm(){
        document.querySelector('#category').value = '';
        document.querySelector('#supplierP').value = '';
        document.querySelector('#product-name').value = '';
        document.querySelector('#brand').value = '';
        document.querySelector('#product-price').value = '';
        document.querySelector('#size').value = '';
        document.querySelector('#weight').value = '';
        document.querySelector('#description').value = ''; 
    };

    //Giving the created row an id
    static renameProductRow(id1){
        const table = document.querySelector('.product-table');
        table.firstChild.setAttribute('id', id1)
    };
    
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

    //Storing new product to the database
    static storeProduct(product){
        //Retrieving the csrftoken
        const csrftoken = (
            document.querySelector('.productForm')
            .querySelector('[name=csrfmiddlewaretoken]').value
        );
        const request = new Request(
            `/productform`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request,{
            method: 'POST',
            mode: 'same-origin', 
            body: JSON.stringify({
                newProduct: product
            })
        })
        .then(response => response.json())
        .then((res) =>{
            console.log(res.message)
            UI.renameProductRow(res.id)
        })
    };

    //Delete Product
    static deleteProduct(id){
        //To get the crsf token
        const csrftoken = getCookie('csrftoken');

        const request = new Request(
            `/productform`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request,{
            method: 'DELETE',
            mode: 'same-origin',
            body: `${id}`
        })
        .then(response => response.json())
        .then((res) =>{
            console.log(res.message)
        })
    };
};

//Event Listener
try {
    
//Display Contact Form
document.querySelector('.addContact').addEventListener('click', ()=>{
    UI.displayContactForm();
});

//Close Contact Form
document.querySelector('.close-Contact').addEventListener('click', ()=>{
    UI.hideContactForm();
});

//Display Product Form
document.querySelector('.addProduct').addEventListener('click', ()=>{
    console.log('click')
    UI.displayProductForm();
});

document.querySelector('.close-Product').addEventListener('click', ()=>{
    UI.hideProductForm();
});

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
        UI.removeRow(tr);

        //Remove from storage
        Store.deleteContact(tr);
    };
});

//Add Product
document.querySelector('.productForm').addEventListener('submit', (event)=>{
    event.preventDefault();
    const category = document.querySelector('#category').value;
    const supplierP =  document.querySelector('#supplierP').value;
    const nameP = document.querySelector('#product-name').value;
    const brand = document.querySelector('#brand').value;
    const price = document.querySelector('#product-price').value;
    const size = document.querySelector('#size').value;
    const weight = document.querySelector('#weight').value;
    const description = document.querySelector('#description').value;

    //Validation

    if (category ==='' || supplierP ==='' || nameP ==='' || brand ==='' || price ==='' || size ==='' || weight ==='' || description === ''){
        alert('Please Fill in all Fields')
    }else {
        //Creating a new Product
        const newProdcut = new Product(category, supplierP, nameP, brand, price, size, weight, description);
        console.log(newProdcut)

        //Add the new product to display
        UI.addProduct(newProdcut);
        //Clear the form fields
        UI.clearProductForm();

        //Add the product to storage
        Store.storeProduct(newProdcut);
    }
});

document.querySelector('.product-table').addEventListener('click', (event)=> {
    if(event.target.classList.contains('delete-product')){
        //Getting the row of the button clicked
        tr = event.target.parentElement.parentElement;
        
        //Delete row from display
        UI.removeRow(tr);

        //Delete Product from the database
        Store.deleteProduct(tr.id);
    }
});

}catch{
    document.querySelector('.addProduct').addEventListener('click', ()=>{
        console.log('click')
        UI.displayProductForm();
    });
    console.log(":}")
}