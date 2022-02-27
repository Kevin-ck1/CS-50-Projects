class Price {
    constructor(product, supplier, price){
        this.product = product;
        this.supplier = supplier;
        this.price = price;
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
};

//Variables
const table = document.querySelector('#pricesTable');
const suppliers = JSON.parse(localStorage.getItem("suppliers"));
const newPriceRow = table.querySelector('#newPriceRow');

//Display Class
class UI{
    static addRow(){
        newPriceRow.style.display = "";
    };

    static addPrice(){
        const supplierId = document.querySelector('#supplier').value;
        const price = document.querySelector('.price').value;
        const product = document.querySelector('.productId').innerText;
        if (supplierId == '' || price == ''){
            alert('Fill in all the fields')
        }else{
            const supplierPrice = new Price(product, supplierId, price)
            const newRow = document.createElement('tr');
            let supplierName;

            for (let supplier of suppliers){
                if(supplier.id == supplierId){
                    supplierName = supplier.nameS
                }
            }

            newRow.innerHTML = 
            `
            <th scope="row" class="rowCounter text-center"></th>
            <td class="text-center" >${supplierName}</td>
            <td class="text-center supplierId" hidden >${supplierPrice.supplier}</td>
            <td class="text-center">${supplierPrice.price}</td>
            <td class="d-flex justify-content-center">
                 <button id="editButton" class="pr-1 btn btn-lg text-dark" >
                    <i class="far fa-edit"></i>
                </button>
                <button id="deleteButton" class="pl-0 btn btn-lg text-dark">
                    <i class="far fa-trash-alt"></i>
                </button>
            </td>
            `
            //Inserting the new price row to the table
            table.insertBefore(newRow, table.lastElementChild);

            //Removing the add field from the table display
            newPriceRow.style.display = "none";

            const rIndex = table.lastElementChild.previousElementSibling.rowIndex
            Store.addPrice(supplierPrice, rIndex)

        }
    };

    static renameRow(rIndex, id){
        const row = table.rows[rIndex-1]
        console.log(row.innerHTML)
        console.log(id)
        row.setAttribute('id', id)
    };

    static editInput(e){
        // var row = '';
        // var priceColumn = ''; 
        // var currentPrice = '';

        if(e.target.parentElement.id == "editButton"){
            //get clicked row
            //const row = e.target.parentElement.parentElement.parentElement.parentElement;
            const row = e.target.closest("tr");
            const priceColumn = row.querySelector('.supplierPrice');
            const currentPrice = priceColumn.innerText;
            localStorage.setItem("currentPrice", currentPrice)
            priceColumn.innerHTML =
             `
                <input type="text" class="editprice" value="${currentPrice}">
            `
            
            const editButton = row.querySelector('#editButton');
            
            editButton.innerHTML =
            `
                <i class="fa fa-check"></i>
            `
            editButton.setAttribute('id', "saveEdit");

            const deleteButton = row.querySelector('#deleteButton');
            deleteButton.innerHTML =
            `
                <i class="fa fa-ban"></i>
            `

            deleteButton.setAttribute('id', "cancelEdit");

        } else if (e.target.parentElement.id == "cancelEdit"){
            //get clicked row
            const row = e.target.closest("tr");
            //Get the price Column
            const priceColumn = row.querySelector('.supplierPrice');
            const currentPrice = localStorage.getItem("currentPrice")
            priceColumn.innerHTML = currentPrice;
            
            const saveEdit = row.querySelector('#saveEdit');
            
            saveEdit.innerHTML =
            `
                <i class="far fa-edit"></i>
            `
            saveEdit.setAttribute('id', "editButton");

            const cancelEdit = row.querySelector('#cancelEdit');
            cancelEdit.innerHTML =
            `
                <i class="far fa-trash-alt"></i>
            `

            cancelEdit.setAttribute('id', "deleteButton");
    
        } else if(e.target.parentElement.id == "saveEdit"){
           //get clicked row
            //const row = e.target.parentElement.parentElement.parentElement.parentElement;
            const row = e.target.closest("tr");
            const priceColumn = row.querySelector('.supplierPrice');
            const editPrice = row.querySelector('.editprice').value;
            
            priceColumn.innerHTML = editPrice;
            
            const saveEdit = row.querySelector('#saveEdit');
            
            saveEdit.innerHTML =
            `
                <i class="far fa-edit"></i>
            `
            saveEdit.setAttribute('id', "editButton");

            const cancelEdit = row.querySelector('#cancelEdit');
            cancelEdit.innerHTML =
            `
                <i class="far fa-trash-alt"></i>
            `

            cancelEdit.setAttribute('id', "deleteButton");
        };


    };
};

//Store Class
class Store {
    static fetchSuppliers(){
        fetch("/company/fetchSuppliers")
        .then(response => response.json())
        .then((res)=>{
            localStorage.setItem("suppliers", JSON.stringify(res.suppliers))
            console.log(JSON.parse(localStorage.getItem("suppliers")))
        })
    };

    static addPrice(price, rIndex){
        const request = requestPath(`productPrice`)
        console.log(request)
        fetch(request, {
            method: "POST",
            mode:"same-origin",
            body: JSON.stringify({
                newPrice: price
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
            //Rename New Price Row
            UI.renameRow(rIndex, res.id)
        })
    }
};

//Events
//Load
window.addEventListener('DOMContentLoaded', ()=>{
    Store.fetchSuppliers();
});

//Add New Price Row
document.querySelector('#addPrice').addEventListener('click', ()=>{
    UI.addRow();
});

//Add New Supplier Price
document.querySelector('#savePrice').addEventListener('click', ()=>{
    UI.addPrice();
});

//Event: Edit/Cancel Button Clicked
table.addEventListener('click', (e)=>{
    UI.editInput(e)
});