//Product Class: 
class Product{
    constructor(nameP, brand, category, size, weight, description){
        this.nameP = nameP;
        this.brand = brand;
        this.category = category;
        this.size = size;
        this.weight = weight;
        this.description = description;
    }
};

class Supply{
    constructor(qty, price, total, product, job, maxPrice, minPrice){
        this.qty = qty;
        this.price = price;
        this.total = total;
        this.product = product;
        this.job = job;
        this.maxPrice = maxPrice;
        this.minPrice = minPrice;
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

//Reload page on back
var perfEntries = performance.getEntriesByType("navigation");

if (perfEntries[0].type === "back_forward") {
    location.reload(true);
}

//Display class

class UI {
    //Add Product Input Row - Using Button
    static addInputRow(){
        document.querySelector('#hiddenRow').style.display = "";
        UI.disableButtons();
    };

    static disableButtons(){
        document.querySelectorAll('#editButton').forEach((b)=>{
            b.disabled = true;
        })
        document.querySelectorAll('#deleteButton').forEach((b)=>{
            b.disabled = true;
        })
        const button = document.querySelector('#addProduct')
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
        const button = document.querySelector('#addProduct')
        button.className = "btn btn-primary"
        button.disabled = false;
    };

    //Create a list that houses the products
    static searchList(){
        //Obtain all the producst available to us
        let products = JSON.parse(localStorage.getItem("products"));

        //Collecting products that already listed in the job
        //First obtaining the product rows
        var rows = document.querySelector('#productTable').rows;
        //Creating an empty array so as to push the existing product ids into it
        const currentProducts = []
        //Adding the ids by iterating
        for(let i=0, length = rows.length; i < length - 1; i++){
            var productId = parseInt(rows[i].id)
            currentProducts.push(productId)
        };

        //Removing the current products from the all products list
        let displayProducts = []
        products.forEach((product)=>{
            if(currentProducts.indexOf(product.id) == -1){
                displayProducts.push(product)
            }
            
        });
        document.querySelectorAll('#searchList').forEach((list)=>{
            displayProducts.forEach((product)=>{
                let li = document.createElement("li")
                li.setAttribute("class", "list-group-item")
                li.setAttribute("id", product.id)
                li.innerHTML = product.nameP
                list.append(li)
                li.style.display = "none"
                li.addEventListener('click', ()=>{
                    UI.addProduct(product, list)
                })
            });
        });
        
    };    
    //Filter functions to filter the required product
    static filterProducts(input){
        //let filterValue = document.querySelector(".filterInput").value.toUpperCase();
        let filterValue = input.value.toUpperCase();
        input.nextElementSibling.querySelectorAll('li').forEach((li)=>{
            let productName = li.innerText.toUpperCase();
            if(productName.indexOf(filterValue) == -1){
                li.style.display = "none";
            }else if(filterValue == ''){
                li.style.display = "none";
            }else{
                li.style.display = "";
            };
        });
    };

    //Add Product To a table
    static addProduct(product, list){
        //Clear Filter
        UI.clearFilter()

        //Clear the searchlist
        document.querySelectorAll('#searchList').forEach((list)=>{
            list.innerHTML = '';
        })

        const productTable = document.querySelector('#productTable')
        const newRow = document.createElement('tr')
        //Getting the price of the selected product
        let prices = JSON.parse(localStorage.getItem("prices"));
        //Get the various prices of the prouct
        let productPrices = prices.filter(x => x.product_id == product.id);

        let maxPrice = Math.max.apply(Math, productPrices.map(x => x.price));
        let minPrice = Math.min.apply(Math, productPrices.map(x => x.price));
        let qty = 1;
        //Calulating the selling price for the product
        let price = (Math.ceil(maxPrice*1.36/5))*5 //Round Up to the nearest 5
        let total = price * qty

        //Fetching the id for the job
        let jobId = parseInt(document.querySelector('.jobId').innerText);
        //Creating a supply object
        const supply = new Supply(qty, price, total, product.id, jobId, maxPrice, minPrice);

        newRow.innerHTML = `
            <th scope="row" class="rowCounter text-center"></th>
            <td id="name" class="text-center" >${product.nameP} : ${product.brand} </td>
            <td id="category" class="text-center">${product.category}</td>
            <td id="qty" class="text-center">${qty}</td>
            <td id="price" class="text-center">${price}</td>
            <td id="total" class="text-center">${total}</td>
            <td class="d-flex justify-content-center">
                <button id="editButton" class="pr-1 btn btn-lg text-dark" >
                    <i class="far fa-edit"></i>
                </button>
                <button id="deleteButton" class="pl-0 btn btn-lg text-dark">
                    <i class="far fa-trash-alt"></i>
                </button>
            </td>
        `

        newRow.setAttribute("id", product.id)
        //Placing the new row into the table
        productTable.insertBefore(newRow, productTable.firstElementChild);

        //Hide the input row field
        document.querySelector('#hiddenRow').style.display = "none";

        //Enable the buttons
        UI.enableButtons();

        //Refresh the search list
        UI.searchList();

        //Store the Product
        Store.storeProducts(supply);

        if (list.parentElement.localName == "td"){
            newRow.querySelector('#editButton').querySelector('i').click()
        }else{
            console.log("Search Bar Clicked")
        }

    };


    //To clear the filter input field
    static clearFilter(){
        //document.querySelector(".filterInput").value = '';  
        document.querySelectorAll(".filterInput").forEach((input)=>{
            input.value = '';
        });
    };

    static productEdits(e){
        let clicked = e.target;
        let row = clicked.closest('tr');
        let clickedButton = clicked.parentElement;
        let qtyCell = row.querySelector('#qty')
        let priceCell = row.querySelector('#price')
        let totalCell = row.querySelector('#total')

        //Setting the buttons as variables
        const editButton = row.querySelector('#editButton');
        const deleteButton = row.querySelector('#deleteButton');

        //console.log(row.cells[2])
        //Obtaining array of the products
        let products = JSON.parse(localStorage.getItem("products"));
        //To get the product id of the row to edit
        let productId = row.id;
        //To get the product in the row to edit
        let product = products.find( x => x.id == productId)
        console.log(product)
        switch(clickedButton.id){
            case "editButton":
                //Placing the qty cell  into edit mode
                qtyCell.innerHTML = `<input type="text" class="qty form-control" value="${qtyCell.innerText}">`;

                //Placing the priceCell under edit
                priceCell.innerHTML = `<input type="text" class="qty form-control" value="${priceCell.innerText}">`;

                //Changing the action buttons
                editButton.innerHTML =` <i class="fa fa-check"></i>`
                editButton.setAttribute('id', "saveEdit");
                deleteButton.innerHTML =`<i class="fa fa-ban"></i>`
                deleteButton.setAttribute('id', "cancelEdit");
                
                //Disable buttons
                UI.disableButtons();

            break;

            case "saveEdit":
                //Getting the vaalues from the input fields

            break;

            case "saveProduct":
                console.log("Save Button Not Working Yet")
            break;
        }
    }
};

//Store Class
class Store{
    //Function for fetching items form the database
    static fetchItems(){
        //Get csrf token
        const csrftoken = getCookie('csrftoken');
        const request = new Request(
            `/company/fetchItems`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        console.log(request)

        fetch(request)
        .then(response=> response.json())
        .then((res)=>{
            localStorage.setItem("products", JSON.stringify(res.products));
            localStorage.setItem("suppliers", JSON.stringify(res.suppliers));
            localStorage.setItem("jobs", JSON.stringify(res.jobs));
            localStorage.setItem("prices", JSON.stringify(res.prices));
        })
        .then(()=>{
            //Place Items into the Search list
            UI.searchList();
        });
    };

    //To delete a job
    static deleteJob(){
        const request = requestPath(``)
        fetch(request,{
            method: "DELETE",
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
        }).then(()=>{
            window.location=`/company/jobs`
        })
    };

    static storeProducts(supply){
        const request = requestPath(`/company/supplies/${supply.product}`)
        console.log(request)
        fetch(request, {
            method: "POST",
            mode:"same-origin",
            body: JSON.stringify({
                newSupply: supply
            })
        })
        .then(response => response.json())
        .then((res)=>{
        })
    }
};

//On Load
window.addEventListener('DOMContentLoaded', ()=>{
    //Fetch Items from the data base
    Store.fetchItems();
    //Clear the filter field
    UI.clearFilter();
});

//Event: Add Product Row -- Method no longer in use
document.querySelector('#addProduct').addEventListener('click', ()=>{
    UI.addInputRow();
});

//Event: Product search throw the filter Field
document.querySelectorAll('.filterInput').forEach((input)=>{
    input.addEventListener('keyup', ()=>{
        UI.filterProducts(input);
    })
}) 

//Delete a job
document.querySelector('#deleteJob').addEventListener('click', ()=>{
    Store.deleteJob();
});

//Event: Edit/Cancel/Delete Product
document.querySelector('#productTable').addEventListener('click', (e)=>{
    if(e.target.parentElement){
        if(e.target.parentElement.cellIndex !== 1){
            UI.productEdits(e);
        };
    };
});
