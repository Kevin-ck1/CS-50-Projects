class Personnel {
    constructor(name, phone, email, companyId, type){
        this.name = name;
        this.phone = phone;
        this.email = email;
        this.companyId = companyId;
        this.type = type
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

//Variables
const modal = document.querySelector('.modal1') //Edit form form variable

//UI Class
class UI{
    static addRow(){
        const table = document.querySelector('#personnelTable')
        const newRow = document.createElement('tr');
        newRow.innerHTML = 
            `
            <th scope="row" class="rowCounter text-center"></th>
            <td class="text-center"><input type="text" class="name"></td>
            <td class="text-center"><input type="text" class="phone"></td>
            <td class="text-center"><input type="text" class="email"></td>
            <td class="d-flex justify-content-center">
                <button id="savePerson" class="pr-1 btn btn-lg text-dark" >
                    <i class="fa fa-check"></i>
                </button>
                <button id="cancelButton" class="pl-0 btn btn-lg text-dark">
                    <i class="fa fa-ban"></i>
                </button>
            </td>
            `;
        table.appendChild(newRow);

        UI.disableButtons();

    };

    static savePerson(person, rIndex){
        const table = document.querySelector('#personnelTable')
        const newRow = document.createElement('tr');
        newRow.innerHTML = 
            `
            <th scope="row" class="rowCounter text-center"></th>
            <td id="name" class="text-center">${person.name}</td>
            <td id="phone" class="text-center">${person.phone}</td>
            <td id="email" class="text-center">${person.email}</td>
            <td class="d-flex justify-content-center">
                <button id="editButton" class="pr-1 btn btn-lg text-dark" >
                    <i class="far fa-edit"></i>
                </button>
                <button id="deleteButton" class="pl-0 btn btn-lg text-dark">
                    <i class="far fa-trash-alt"></i>
                </button>
            </td>
            `;

        if (rIndex){
            const oldRow = table.rows[rIndex-1];
            oldRow.replaceWith(newRow);
        }else {
            UI.removeRow(table.lastElementChild)
            table.appendChild(newRow);
        }

        UI.enableButtons();
        
    }

    static removeRow(row){
        row.remove();
    };

    static editForm(tr){
        const name = tr.querySelector('#name').innerHTML;
        const phone = tr.querySelector('#phone').innerHTML;
        const email = tr.querySelector('#email').innerHTML;

        const person = {name:name, phone:phone, email:email};
        localStorage.setItem("person", JSON.stringify(person))
        

        tr.innerHTML = 
            `
            <th scope="row" class="rowCounter text-center"></th>
            <td class="text-center"><input type="text" class="name" value="${name}"></td>
            <td class="text-center"><input type="text" class="phone" value="${phone}"></></td>
            <td class="text-center"><input type="text" class="email" value="${email}"></></td>
            <td class="d-flex justify-content-center">
                <button id="editPerson" class="pr-1 btn btn-lg text-dark" >
                    <i class="fa fa-check"></i>
                </button>
                <button id="cancelEdit"class="pl-0 btn btn-lg text-dark">
                    <i class="fa fa-ban"></i>
                </button>
            </td>
            `;

        UI.disableButtons();
    }

    static disableButtons(){
        document.querySelectorAll('#editButton').forEach((b)=>{
            b.disabled = true;
        })
        document.querySelectorAll('#deleteButton').forEach((b)=>{
            b.disabled = true;
        })
        const button = document.querySelector('#addPerson')
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
        const button = document.querySelector('#addPerson')
        button.className = "btn btn-primary"
        button.disabled = false;
    };

    static renameRow(rIndex, id){
        const table = document.querySelector('#personnelTable')
        const row = table.rows[rIndex-1]
        console.log(row.innerHTML)
        row.setAttribute('id', id)
    };

    static removePerson(tr){
        tr.remove()
    };

     //Zones: Display the String Value for zones
    static displayZone(){
        const zone = document.querySelector('.sZone').innerHTML;
        const zones = ["Zone 1: CBD", "Zone 2: Down Town", "Zone 3: Industrial Area"]
        if(parseInt(zone)){
            document.querySelector('.sZone').innerHTML = zones[zone - 1];
        };
    };

    //Open Supplier Form
    static editSupplier(){
        modal.style.display = "block";
    };

    //Close Supplier Form
    static closeForm(){
        modal.style.display = "none";
    };

    static displayPersonnels(){
        document.querySelector('#personnel').style.display = "block";
        const b = document.querySelector('.showPersonnel');
        b.className = "hidePersonnel";
        b.innerHTML = "Hide Personnel";
    };
    
    static hidePersonnels(){
        document.querySelector('#personnel').style.display = "none";
        const b = document.querySelector('.hidePersonnel');
        b.className = "showPersonnel";
        b.innerHTML = "Show Personnel";

        UI.disableButtons();
    }
};

//Storage Class
class Store{
    static storePerson(person,rIndex){
        const request = requestPath(`personnel`);
        console.log(request)
        fetch(request, {
            method: "POST",
            mode: "same-origin",
            body: JSON.stringify({
                newPerson: person
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
            //Rename New Product Row
            UI.renameRow(rIndex, res.id)
        })
    };

    static updatePerson(person, rIndex, id){
        const request = requestPath(`personnel`);
        console.log(request)
        fetch(request, {
            method: "PUT",
            mode: "same-origin",
            body: JSON.stringify({
                updatePerson: person,
                personId: id
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
            //Rename New Product Row
            UI.renameRow(rIndex, id);
        })
    };

    static deletePerson(id){
        const request = requestPath(`personnel`);
        console.log(request)
        fetch(request, {
            method: "DELETE",
            mode: "same-origin",
            body: JSON.stringify({
                personId: id
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
        })
    };

    static deleteSupplier(){
        const url = window.location.href;
        const supplierId = document.querySelector('.sId').innerHTML;
        const supplierName = document.querySelector('.sName').innerHTML;
        const request = requestPath(``);

        console.log(request)

        fetch(request, {
            method: "DELETE",
            mode: "same-origin",
            body: JSON.stringify({
                supplierId: supplierId,
                supplierName: supplierName
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
        })
        .then(()=>{
            window.location=`/company/suppliers`
        })
        
    };
}
//Events
//Generate New table Row
document.querySelector('#addPerson').addEventListener('click',()=>{
    UI.addRow()
});

//Add/edit Person Event
document.querySelector('#personnelTable').addEventListener('click', (e)=>{
    if(e.target.parentElement.id == "savePerson" || e.target.parentElement.id == "editPerson"){
        console.log(e.target)
        const row = e.target.parentElement.parentElement.parentElement
        const rIndex = row.rowIndex;
        const rowId = row.id;
        const name = document.querySelector('.name').value;
        const phone = document.querySelector('.phone').value;
        const email = document.querySelector('.email').value;
        const url = window.location.href;
        const companyId = url.split("/").pop();
        const type = "supplier";

        if(name == "" || phone == "" || email == ""){
            alert('Please Fill In All The Fields')
        }else {
            //Creating a new instance of a person
            const person = new Personnel(name, phone, email, companyId, type);
            if(e.target.parentElement.id == "savePerson" || e.target.id == "savePerson"){
                //Add the person to the display
            UI.savePerson(person);

            //Store the Person to the database
            Store.storePerson(person, rIndex);

            }else{
                console.log("Edit Mode")
                UI.savePerson(person, rIndex);
                Store.updatePerson(person, rIndex, rowId);
            }
        }
    }
});

//Event: Cancel Button
document.querySelector('#personnelTable').addEventListener('click', (e)=>{
    if(e.target.parentElement.id == "cancelButton"){
        const row = e.target.parentElement.parentElement.parentElement;
        UI.removeRow(row);
        UI.enableButtons();
    }
})
//Event: Edit Person
document.querySelector('#personnelTable').addEventListener('click', (e)=>{
    if(e.target.parentElement.id == "editButton" ){
        const row = e.target.parentElement.parentElement.parentElement;
        UI.editForm(row);
    }
})


//Event: Cancel Edit
document.querySelector('#personnelTable').addEventListener('click', (e)=>{
    if(e.target.parentElement.id == "cancelEdit"){
        const row = e.target.parentElement.parentElement.parentElement;
        const rIndex = row.rowIndex;
        const rowId = row.id;
        const person = JSON.parse(localStorage.getItem("person"))
        
        UI.savePerson(person, rIndex)
        UI.renameRow(rIndex, rowId);
        UI.enableButtons();
    }
});

//Event: Delete Person
document.querySelector('#personnelTable').addEventListener('click', (e)=>{
    if (e.target.parentElement.id == "deleteButton"){
        const tr = e.target.parentElement.parentElement.parentElement;
        const personId = tr.id;

        //Remove row from display
        UI.removePerson(tr);

        //Remove person from data base
        Store.deletePerson(personId);
    };
});

//On Loading the Page
document.addEventListener('DOMContentLoaded', ()=>{
    //Display the Zones in propere format
    UI.displayZone();

    //Diable the add personnel Button
    UI.disableButtons();
});

//Deleting A Supplier
document.querySelector('#deletesupplier').addEventListener('click', ()=>{
    Store.deleteSupplier();
});

//Editing A Supplier
document.querySelector('#editsupplier').addEventListener('click', ()=>{
    UI.editSupplier();
})

//Closing the supplier Form
document.querySelector('.closeButton').addEventListener('click', ()=>{
    UI.closeForm();
})

window.addEventListener('click',(e)=>{
    
    if(e.target == modal){
        UI.closeForm();
    }
});

//To Display and hide the personnels table
document.querySelector('#personnelSection').addEventListener('click', (e)=>{
    if(e.target.className == "showPersonnel"){
        UI.enableButtons();
        UI.displayPersonnels();
    } else if(e.target.className == "hidePersonnel"){
        UI.hidePersonnels();
    }
})




