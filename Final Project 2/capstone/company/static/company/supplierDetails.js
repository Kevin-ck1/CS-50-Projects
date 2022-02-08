//Contact Personnel
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
                <button class="pl-0 btn btn-lg text-dark">
                    <i class="far fa-trash-alt"></i>
                </button>
            </td>
            `;
        table.appendChild(newRow);

        const button = document.querySelector('#addPerson')
        button.className = "btn btn-secondary"
        button.disabled = true;

    };

    static addPerson(person){
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
        UI.removeRow(table.lastElementChild)
        table.appendChild(newRow);

        const button = document.querySelector('#addPerson')
        button.className = "btn btn-primary"
        button.disabled = false;
    }

    static removeRow(row){
        row.remove();
    };

    static editForm(tr){
        const name = tr.querySelector('#name').innerHTML;
        const phone = tr.querySelector('#phone').innerHTML;
        const email = tr.querySelector('#email').innerHTML;

        tr.innerHTML = 
            `
            <th scope="row" class="rowCounter text-center"></th>
            <td class="text-center"><input type="text" class="name" value="${name}"></td>
            <td class="text-center"><input type="text" class="phone" value="${phone}"></></td>
            <td class="text-center"><input type="text" class="email" value="${email}"></></td>
            <td class="d-flex justify-content-center">
                <button id="savePerson" class="pr-1 btn btn-lg text-dark" >
                    <i class="fa fa-check"></i>
                </button>
                <button class="pl-0 btn btn-lg text-dark">
                    <i class="far fa-trash-alt"></i>
                </button>
            </td>
            `;
    }
}

//Storage Class
class Store{
    static storePerson(person){
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
        })
    }
}
//Events
//Generate New table Row
document.querySelector('#addPerson').addEventListener('click',()=>{
    UI.addRow()
})


//Add Person Event
document.querySelector('#personnelTable').addEventListener('click', (e)=>{
    if(e.target.parentElement.id == "savePerson" || e.target.id == "savePerson"){
        console.log(e.target)
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
            //Add the person to the display
            UI.addPerson(person);

            //Store the Person to the database
            Store.storePerson(person);

        }
    }
});

//Event: Edit Person
document.querySelectorAll('#editButton').forEach((b)=>{
    b.addEventListener('click', ()=>{
        const row = b.parentElement.parentElement;
        UI.editForm(row);
    })
})
