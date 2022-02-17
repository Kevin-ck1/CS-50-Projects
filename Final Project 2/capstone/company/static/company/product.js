
//Product Class: 
class Product{
    constructor(nameP, brand, category, productPrice, size, weight, supplier, description){
        this.nameP = nameP;
        this.brand = brand;
        this.category = category;
        this.productPrice = productPrice;
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

        //Closing form
        UI.closeForm();

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

    //To rename the new product row
    static renameRow(id){
        const table = document.querySelector('#tableProduct')
        console.log(table.firstElementChild)
        const row = table.firstElementChild
        row.setAttribute('id', id)
        row.addEventListener('click',()=>{
            UI.prodcutDetails(id)
        })

    }

    //To close the update field
    static finishUpdate(product){
        console.log(product.nameP)
        //window.location=`/company/products/${id}`;
        document.querySelector('#nameP').previousElementSibling.innerHTML = product.nameP;
        document.querySelector('#category').previousElementSibling.innerHTML = product.category;
        document.querySelector('#brand').previousElementSibling.innerHTML = product.brand;
        document.querySelector('#size').previousElementSibling.innerHTML = product.size;
        document.querySelector('#weight').previousElementSibling.innerHTML = product.weight;
        document.querySelector('#description').previousElementSibling.innerHTML = product.description;

        document.querySelectorAll('.pdetail').forEach((i)=>{
            i.style.display = '';
        });
        document.querySelectorAll('.inputUpdate').forEach((i)=>{
            i.style.display = 'none';
            
        });

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
            //Rename New Product Row
            UI.renameRow(res.id);
        })
    };

    static updateProduct(id, product){
        const csrftoken = getCookie('csrftoken');
        const request = new Request (
            `${id}`,
            {headers: {'X-CSRFToken': csrftoken}}
        )

        fetch(request, {
            method: "PUT",
            mode: "same-origin",
            body: JSON.stringify({
                editedProduct: product
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
        }).then(()=>{
            
        })
    };

    

    static deleteProduct(id){
        
        const csrftoken = getCookie('csrftoken');
        const request = new Request (
            `${id}`,
            {headers: {'X-CSRFToken': csrftoken}}
        )

        fetch(request, {
            method: "DELETE",
            mode: "same-origin",
            body:`${id}` 
        })
        .then(response => response.json())
        .then((res) =>{
            console.log(res.message)
        })
        .then(()=>{
            window.location=`/company/products`
        })
    }
}


try {
    //Event, addButton click
    document.querySelector('#addButton').addEventListener('click',()=>{UI.openForm()});

    //Event, close button click
    document.querySelector('.buttonClose').addEventListener('click', ()=>{UI.closeForm()})

    //Event, submiting form
    document.querySelector('#productForm').addEventListener('submit', (event)=>{
        event.preventDefault();
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
   //Event, Activate Edit Mode 
    document.querySelector('#editProduct').addEventListener('click', ()=>{
        document.querySelectorAll('.pdetail').forEach((detail)=>{
            detail.style.display = 'none';
        })
        document.querySelectorAll('.inputUpdate').forEach((i)=>{
            i.style.display = '';
            
        });
    }); 

    //Submit Form, to update product details
    document.querySelector('#updateProduct').addEventListener('click', (e)=>{
        e.preventDefault();
        console.log('Update Submitted')
        const nameP = document.querySelector('#nameP').value;
        const brand = document.querySelector('#brand').value;
        const category = document.querySelector('#category').value;
        //const price = document.querySelector('#price').value;
        const size = document.querySelector('#size').value;
        const weight = document.querySelector('#weight').value;
        //const supplier = document.querySelector('#supplier').value;
        const description = document.querySelector('#description').value;

        const url = window.location.href;
        const productId = url.split("/").pop();
        const newProduct = new Product(nameP, brand, category,  size, weight, description); 

        Store.updateProduct(productId, newProduct);
        UI.finishUpdate(newProduct);
        
    })

    //Event, Deleting A product
    document.querySelector('#deleteProduct').addEventListener('click', ()=>{
        const url = window.location.href;
        const productId = url.split("/").pop();

        Store.deleteProduct(productId);
    })
}





