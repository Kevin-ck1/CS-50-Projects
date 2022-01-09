
//Product Class: 
class Product{
    constructor(nameP, brand, category, price, size, weight, supplier, description){
        this.nameP = nameP;
        this.brand = brand;
        this.category = category;
        this.price = price;
        this.size = size;
        this.weight = weight;
        this.description = description;
        this.supplier = supplier;
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

//UI Class: UserInterface
class UI {

    //To display the form
    static openForm(){
        var form = document.querySelector('.productForm');
        form.style.display = 'block';
        form.classList.add('card');
    }

    //To close the form
    static closeForm(){
        var form = document.querySelector('.productForm');
        form.style.display = 'none';
        form.classList.remove('card');
    }

    //Adding the new Product to the display
    static addProduct(product){
        const table = document.querySelector('#tableProduct');
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td scope="row" class="rowCounter"></td>
            <td>${product.nameP}</td>
            <td>${product.brand}</td>
            <td>${product.price}</td>
        `;


        //Placing the new row into the table
        table.insertBefore(newRow, table.firstElementChild);

    }

    static clearForm(){
        document.querySelector('#nameP').value = '';
        document.querySelector('#brand').value = '';
        document.querySelector('#category').value = '';
        document.querySelector('#price').value = '';
        document.querySelector('#size').value = '';
        document.querySelector('#weight').value = '';
        document.querySelector('#supplier').value = '';
        document.querySelector('#description').value = '';
    };

    //To redirect to the product details
    static prodcutDetails(id){
        window.location=`/company/products/${id}`;

    }
};

class Store {
    static storeProduct(product){
        //Get csrf token
        const csrftoken = getCookie('csrftoken');
        const request = new Request(
            `/company/productform`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request, {
            method: "POST",
            mode: 'same-origin',
            body: JSON.stringify({
                newProduct: product
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
        })
    };
}

try {
    //Event, addButton click
    document.querySelector('#addButton').addEventListener('click',()=>{UI.openForm()});

    //Event, close button click
    document.querySelector('.buttonClose').addEventListener('click', ()=>{UI.closeForm()})

    //Event, submiting form
    document.querySelector('#productForm').addEventListener('submit', (event)=>{
        event.preventDefault();
        console.log('Form Submitted')
        const nameP = document.querySelector('#nameP').value;
        const brand = document.querySelector('#brand').value;
        const category = document.querySelector('#category').value;
        const price = document.querySelector('#price').value;
        const size = document.querySelector('#size').value;
        const weight = document.querySelector('#weight').value;
        const supplier = document.querySelector('#supplier').value;
        const description = document.querySelector('#description').value;

        //Validating the form
        if(nameP=='' || brand == ''|| category == ''|| category==''|| price == ''|| size==''|| weight==''|| supplier==''|| description=='' ){
            alert('Please Fill In all fields')
        }else {
            //Creating a new instance of the product
            const newProduct = new Product(nameP, brand, category, price, size, weight, supplier, description);
            //Add The new product to the display
            UI.addProduct(newProduct);

            //Add the new product to the database
            Store.storeProduct(newProduct);

            //Clear the form fields
            UI.clearForm();
        }

        
    })

    // Event, row(product) click
    document.querySelectorAll('tr').forEach((r)=>{
        r.addEventListener('click', ()=>{
            UI.prodcutDetails(r.id);
        })
    });

} catch {
   //Event, Update product details
    document.querySelector('#updateProduct').addEventListener('click', ()=>{
        console.log('Update Button Clicked')
        document.querySelectorAll('.pdetail').forEach((detail)=>{
            detail.style.display = 'none';
        })
    }); 
}





