
//Job Class: 
class Job{
    constructor(code, client, product, value, status){
        this.code = code;
        this.client = client;
        this.product = product;
        this.value = value;
        this.status = status;
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

function requestPath(url){
    //Get csrf token
    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        `${url}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    return request;
}


//Reload page on browser navigation
window.addEventListener("pageshow", (event)=>{
    const hist = event.persisted || window.performance.navigation.type == 2 
    if(hist){
        window.location.reload(true);
    }
});

//Variables
const categories = ["ICT", "Electricity", "Hairdressing", "Hospitality", "Plumbing & Masonry", "Stationary"]
const status = ["RFQ", "LPO", "Supplied", "Paid"] 

//UI Class: UserInterface
class UI {
    //To display the form
    static openForm(){
        var form = document.querySelector('.jobForm');
        form.style.display = 'block';
        form.classList.add('card');
    }

    //To close the form
    static closeForm(){
        var form = document.querySelector('.jobForm');
        form.style.display = 'none';
        form.classList.remove('card');
    }

    static clearForm(){
        document.querySelector('#jobCode').value = '';
        document.querySelector('#client').value = '';
    };

    //To redirect to the jobs details
    static jobDetails(id){
        var jobs = JSON.parse(localStorage.getItem("jobs"))
        var ids = [];
        for (let job of jobs){
            ids.push(job.id)
        }
        if(ids.includes(parseInt(id))){
            window.location=`jobs/${id}`
        }else{
            alert("Queried Job Does Not Exist")
        }
    };

    static filterJobs(){
        let filterValue = document.querySelector('.filterInput').value.toUpperCase();
        
        console.log(filterValue);

        document.querySelector('#jobTable').querySelectorAll('tr').forEach((tr)=>{
            let productName = tr.querySelector('td').nextElementSibling.innerText.toUpperCase();
            if (productName.indexOf(filterValue) > -1){
                tr.style.display = '';
            }else {
                tr.style.display = "none";
            }
            
        });
    };

    static jobCheck(){
        const code = document.querySelector('#jobCode').value;
        const client = document.querySelector('#client').value;
        const jobs = JSON.parse(localStorage.getItem("jobs"))
        const message = document.querySelector('.jobWarning')
        const pMessage = message.querySelector('a')
        for (let job of jobs){
            if(job.code == code && job.client_id == client){
                console.log('Match identified');
                message.style.display = "block";
                pMessage.innerHTML = `${code}`;
                pMessage.href = `/company/jobs/${job.id}`;
                UI.disableButtons();
                break;
            }else{
                message.style.display = "none";
                pMessage.innerHTML = ``;
                pMessage.href = ``;
                UI.enableButtons();
            };
        };
    };

    static enableButtons(){
        let button = document.querySelector('#submitButton')
        button.className = "btn btn-primary";
        button.disabled = false;
    };

    static disableButtons(){
        let button = document.querySelector('#submitButton')
        button.disabled = true;
        button.className = "btn btn-secondary";
    };

};

class Store {
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
            //localStorage.setItem("products", JSON.stringify(res.products));
            //localStorage.setItem("suppliers", JSON.stringify(res.suppliers));
            localStorage.setItem("jobs", JSON.stringify(res.jobs));
        })

    };

    static storeJob(job){
        //Get requestPath
        const request = requestPath(``);

        fetch(request, {
            method: "POST",
            mode: 'same-origin',
            body: JSON.stringify({
                newJob: job
            })
        })
        .then(response => response.json())
        .then((res)=>{
            console.log(res.message)
            //UI.jobDetails();
        })
    };

    
}

//Events

//Event, Load Products
window.addEventListener('DOMContentLoaded', ()=>{
    //Fetch products
    Store.fetchItems();
    //Clear the form fields
    UI.clearForm();

    //Enable Buttons
    UI.enableButtons();
})

//Event, addButton click
document.querySelector('#addButton').addEventListener('click',()=>{UI.openForm()});

//Event, close button click
document.querySelector('.buttonClose').addEventListener('click', ()=>{UI.closeForm()})

//Event, submiting form
document.querySelector('#jobForm').addEventListener('submit', (event)=>{
    event.preventDefault();
    const code = document.querySelector('#jobCode').value;
    const client = document.querySelector('#client').value;

    //Validating the form
    if(code == ''|| client ==''){
        alert('Please Fill In all fields')
    }else {
        //Creating a new instance of the product
        const newJob = new Job(code, client);

        //Add the new product to the database
        Store.storeJob(newJob);

        //Clear the form fields
        UI.clearForm();

    };

    
});

// Event, row(product) click
document.querySelectorAll('tr').forEach((r)=>{
    r.addEventListener('click', ()=>{
        UI.jobDetails(r.id);
    })
});


//Event, Filter List
document.querySelector('.filterInput').addEventListener('keyup', ()=>{
    UI.filterJobs();
});


//Event, Check if Product Already Exits
document.querySelector('#client').addEventListener('click',()=>{
    UI.jobCheck();
});
document.querySelector('#jobCode').addEventListener('keyup',()=>{
    UI.jobCheck();
})








