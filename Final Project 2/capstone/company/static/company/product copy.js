
//UI Class: UserInterface
class UI {

    //Adding the new Product to the display
    static addProduct(product){
        const table = document.querySelector('#tableProduct');
        const newRow = document.createElement('tr');
        newRow.innerHtml = `
            <td scope="row" class="rowCounter"></td>
            <td>Camera</td>
            <td>Sony</td>
            <td>10000</td>
        `;

        console.log(table.firstElementChild);

        //Placing the new row into the table
        //table.insertBefore(newRow, table.firstElementChild);
        //table.insertBefore(newRow, table.firstChild);
        table.appendChild(newRow);
        console.log(newRow.innerHtml)
    }
}


document.querySelector('#productForm').addEventListener('submit', (event)=>{
    event.preventDefault();
    UI.addProduct(newProduct);
})

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
        console.log(newProduct);

        //Add The new product to the display
        UI.addProduct(newProduct);
    }

    
})

    //Add product 

