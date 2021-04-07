//Book Class:Represents a Book
        //Every time we create a book it will initiate a book object
class Book {
    constructor(tittle, author, isbn){
        this.tittle = tittle;
        this.author = author;
        this.isbn = isbn;
    }
}

// UI Class: Handles UI tasks, everything that is displayed to the user
//Methods will be static
class UI {
    //To display books
    static displayBooks() {
        //First we import the books from the local storage
        //In this case we use the below dictionary since our storage is empty
        const StoredBooks = [
            {
                tittle: 'Book One',
                author: 'John Doe',
                isbn: '343434'
            },
            {
                tittle: 'Book Two',
                author: 'Jane Doe',
                isbn: '354545'
            }
        ]

        //const books = StoredBooks

        //To get the books from the local storage
        const books = Store.getBooks();

        //Call method to add the fetched books to list, to display the book in the row
        //For each book in storage intiate a method to add it to the table in display
        books.forEach((book)=> {
            UI.addBookToList(book)
        });
    }

    static addBookToList(book){
        const list = document.querySelector('#book-list');

        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${book.tittle}</td>
            <td>${book.author}</td>
            <td>${book.isbn}</td>
            <td><a href="#" class="btn btn-danger btn-sm delete">X</a></td>
        `
        list.appendChild(row);
    }

    //To clear the fields after submit
    static clearFields() {
        document.querySelector('#title').value = '';
        document.querySelector('#author').value = '';
        document.querySelector('#isbn').value = '';
    }

    //To delete Book
    static deleteBook(element) {
        //Check if the item click has the delete class
        if (element.classList.contains('delete')){
            //We are to remove the parent of the selected element
            element.parentElement.parentElement.remove();
        }
    }

    //To show an alert e.g alert for validation error
    static showAlert(message, className){
        const div = document.createElement('div');
        div.className = `alert alert-${className}`;
        div.appendChild(document.createTextNode(message));

        //Place the create element in container above the form
        const container = document.querySelector('.container');
        const form = document.querySelector('#book-form');
        container.insertBefore(div, form)

        //Removing the div after 3seconds
        //setTimeout(()=> document.querySelector('.alert').remove(), 3000); 
        setTimeout(()=> div.remove(), 3000); 

    }
}

//Store Class:Handles Storage
class Store {
    static getBooks(){
        let books;
        //Check if similar book in local storage
        if (localStorage.getItem('books') === null){
            books = [];
        } else {
            //Change the items into an object, since getItems returns a string
            books = JSON.parse(localStorage.getItem('books'));
        }

        return books;
    }

    static addBook(book) {
        //get the list of books from local storage
        const books = Store.getBooks();
        //add the a book to the list of books
        books.push(book);

        //update the books variable in the local storage
        //Since local storage stores data in a string we will use stringify to change the object back to a string
        localStorage.setItem('books', JSON.stringify(books))
    }

    static removeBook(isbn){
        //get the list of books from local storage
        const books = Store.getBooks();

        //Iterate through the list to get the book to delete
        books.forEach((book, index) => {
            if (book.isbn === isbn){
                books.splice(index, 1);
            }
        });

        //Update the local storage
        localStorage.setItem('books', JSON.stringify(books))
    }
}


//Events: Display Book
document.addEventListener('DOMContentLoaded', UI.displayBooks);


//Events: Add a Book
document.querySelector('#book-form').addEventListener('submit', (event)=> {
    event.preventDefault();
    //Get Form values
    const title = document.querySelector('#title').value;
    const author = document.querySelector('#author').value;
    const isbn = document.querySelector('#isbn').value;

    //Validation
    if(title==='' || author === '' || isbn === ''){
        UI.showAlert('Please Fill all Fields', 'danger')
    } else {
        //Instantiate Book: Create a book object from the above data
        const book = new Book(title, author, isbn);

        //Add Book to UI
        UI.addBookToList(book);

        //Add Book to Storage
        Store.addBook(book)

        //Display alert for success
        UI.showAlert('Book Added', 'success')

        //Clear Fields After submit
        UI.clearFields();

    } 
});


//Event: Remove a Book
//We use event propagation, we target the parent then the selected element
//In this case will target the tbody then the row we want to delete.
//event.target get the element select.

document.querySelector('#book-list').addEventListener('click', (event) => {
    //Pass the targeted element to UI for deletion
    UI.deleteBook(event.target);

    //Remove Book from Storage
    Store.removeBook(event.target.parentElement.previousElementSibling.textContent);

    //Display alert for success
    UI.showAlert('Book Removed', 'success')
});