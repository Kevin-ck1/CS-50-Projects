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
    //Generate the input field to add new supplier prices.
    static addRow(){
        newPriceRow.style.display = "";
        UI.disableButtons();
    };

    //To filter the items in the droplist
    static dropDownValues(){
        const rows = table.querySelectorAll('tr')
        
        //Collect suppliers that have already been listed
        var suppliers = [];
        for (let i = 0, length = rows.length; i < length-1; i++){
            var supplier = rows[i].querySelector('td').innerText;
            suppliers.push(supplier)
        }

        //Filter the drop down list to exclude suppliers that are already listed
        var lastRow = rows.item(rows.length-1)
        var options = lastRow.querySelectorAll('#supplierName')
        options.forEach((option)=>{
            var supplierOption = option.innerText;
            console.log(supplierOption)
            if(suppliers.includes(supplierOption)){
                option.style.display = "none";
            }
        })
        
    }

    //Add new supplier price
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
        row.setAttribute('id', id)
    };

    static editInput(e){
        //get clicked row
        //const row = e.target.parentElement.parentElement.parentElement.parentElement;
        var row = e.target.closest("tr");
        var priceColumn = row.querySelector('.supplierPrice');
        var buttonName = e.target.parentElement.id;

        if(buttonName == "editButton"){
            //Get the current price of the item
            var currentPrice = priceColumn.innerText;
            //Store the current price to the local storage
            localStorage.setItem("currentPrice", currentPrice)
            //Create an input field for the change of the price
            priceColumn.innerHTML =
             `
                <input type="text" class="editprice" value="${currentPrice}">
            `
            
            //Changing the action buttons
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
            
            //Disable buttons
            UI.disableButtons();

        //To cancel a price edit: To close the input field    
        } else if (buttonName == "cancelEdit"){
            //Get the stored current price
            const currentPrice = localStorage.getItem("currentPrice")
            priceColumn.innerHTML = currentPrice;
            
            //Changing back the action buttons
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
    
            //To reenable the buttons
            UI.enableButtons();
        //To save changed price    
        } else if(buttonName == "saveEdit"){
            //To get the new price
            const editPrice = row.querySelector('.editprice').value;
            //Display the new price
            priceColumn.innerHTML = editPrice;

            //Save the new price to the data base
            Store.updatePrice(editPrice, row.id)
            
            //Changing back the action buttons
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

             //To reenable the buttons
             UI.enableButtons();

        } else if (buttonName == "cancelButton"){
            newPriceRow.style.display = "none";
        } else if (buttonName == "deleteButton") {
            const rowId = row.id
            row.remove()
            Store.deletePrice(rowId)

             //To reenable the buttons
             UI.enableButtons();
        }
    };

    static disableButtons(){
        document.querySelectorAll('#editButton').forEach((b)=>{
            b.disabled = true;
        })
        document.querySelectorAll('#deleteButton').forEach((b)=>{
            b.disabled = true;
        })
        const button = document.querySelector('#addPrice')
        button.className = "btn btn-secondary"
        button.disabled = true;
    }

    static enableButtons(){
        document.querySelectorAll('#editButton').forEach((b)=>{
            b.disabled = false;
        })
        document.querySelectorAll('#deleteButton').forEach((b)=>{
            b.disabled = false;
        })
        const button = document.querySelector('#addPrice')
        button.className = "btn btn-primary"
        button.disabled = false;
    };
};


//Store Class
class Store {
    static fetchSuppliers(){
        fetch("/company/fetchSuppliers")
        .then(response => response.json())
        .then((res)=>{
            localStorage.setItem("suppliers", JSON.stringify(res.suppliers))
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
    };

    static updatePrice(price, id){
        console.log(`${price}: ${id}`)
        const request = requestPath(`productPrice`)
        console.log(request)
        fetch(request, {
            method: "PUT",
            mode:"same-origin",
            body: JSON.stringify({
                editPrice: price,
                priceId: id
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
        })
    };

    static deletePrice(id){
        const request = requestPath(`productPrice`)
        console.log(request)
        fetch(request, {
            method: "DELETE",
            mode:"same-origin",
            body: JSON.stringify({
                priceId: id
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
        })
    }
};

//Events
//Load
window.addEventListener('DOMContentLoaded', ()=>{
    Store.fetchSuppliers();
    UI.dropDownValues();
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