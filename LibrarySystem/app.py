from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Book class representing a book in the library
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

    def check_out(self):
        if self.available:
            self.available = False
            return True
        return False

    def check_in(self):
        if not self.available:
            self.available = True
            return True
        return False

# LibraryDB class to manage the collection of books
class LibraryDB:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_books(self):
        return self.books

# Initialize the LibraryDB
library = LibraryDB()

@app.route('/')
def index():
    return render_template('index.html', books=library.display_books())

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    
    # Add the book to the library
    book = Book(title, author, isbn)
    library.add_book(book)
    
    flash(f'Book "{title}" added successfully!')
    return redirect(url_for('index'))

@app.route('/manage', methods=['POST'])
def manage_books():
    isbn = request.form['isbn']
    member_name = request.form['member_name']
    action = request.form['action']
    
    # Search for the book in the library
    book = library.search_book(isbn)
    if book:
        if action == 'issue':
            if book.check_out():
                flash(f'Book "{book.title}" has been issued to {member_name}.')
            else:
                flash(f'Book "{book.title}" is not available for issue.')
        elif action == 'return':
            if book.check_in():
                flash(f'Book "{book.title}" has been returned by {member_name}.')
            else:
                flash(f'Book "{book.title}" was not issued.')
    else:
        flash('Book not found.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
