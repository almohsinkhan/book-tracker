import os
from flask import Flask, request, redirect, url_for, render_template, flash, abort # type: ignore
from flask_pymongo import PyMongo # type: ignore
from dotenv import load_dotenv # type: ignore
from form import BookForm, UpdateBookForm
import uuid
import certifi # type: ignore

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

# Initialize PyMongo with system CA bundle
mongo = PyMongo(app, tlsCAFile=certifi.where())


# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    form.user_id.data = 'user001'
    if form.validate_on_submit():
        book = {
            'book_id': str(uuid.uuid4()),
            'user_id': form.user_id.data,
            'title': form.title.data,
            'author': form.author.data,
            'current_page': form.current_page.data,
            'status': form.status.data,
            'notes': form.notes.data
        }
        try:
            mongo.db.books.insert_one(book)
            flash('Book added successfully!', 'success')
        except Exception as e:
            flash(f'Database error: {e}', 'danger')
        return redirect(url_for('get_books', user_id=book['user_id']))
    return render_template('add_book.html', form=form)

@app.route('/books/<user_id>')
def get_books(user_id):
    try:
        books = list(mongo.db.books.find({'user_id': user_id}, {'_id': 0}))
    except Exception as e:
        flash(f'Database error: {e}', 'danger')
        books = []
    return render_template('books.html', books=books)

@app.route('/update_book/<book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = mongo.db.books.find_one({'book_id': book_id})
    if not book:
        abort(404)
    form = UpdateBookForm(data=book)
    if form.validate_on_submit():
        updates = {
            'current_page': form.current_page.data or book['current_page'],
            'status': form.status.data or book['status'],
            'notes': form.notes.data or book['notes']
        }
        try:
            mongo.db.books.update_one({'book_id': book_id}, {'$set': updates})
            flash('Book updated!', 'success')
        except Exception as e:
            flash(f'Database error: {e}', 'danger')
        return redirect(url_for('get_books', user_id=book['user_id']))
    return render_template('update_book.html', form=form, book=book)

@app.route('/remove_book/<book_id>', methods=['POST'])
def remove_book(book_id):
    user_id = request.form.get('user_id', 'user001')
    try:
        result = mongo.db.books.delete_one({'book_id': book_id})
        if result.deleted_count:
            flash('Book removed.', 'success')
        else:
            flash('Book not found.', 'warning')
    except Exception as e:
        flash(f'Database error: {e}', 'danger')
    return redirect(url_for('get_books', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)
