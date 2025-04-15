from flask import Flask, request, jsonify, render_template,  url_for, redirect 
from pymongo import MongoClient
import uuid  # at the top of the file
from urllib.parse import quote_plus
from pymongo import MongoClient

app = Flask(__name__)

username = "almohsinkhan"
password = quote_plus("Mohsin@2004")  # Safely encode special characters

uri = f"mongodb+srv://{username}:{password}@cluster0.p9l28pn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client["book_tracker_db"]
books_collection = db["books"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        data = request.form
        book = {
    "book_id": str(uuid.uuid4()),
    "user_id": data["user_id"],
    "title": data["title"],
    "author": data["author"],
    "current_page": int(data["current_page"]),
    "status": data["status"],
    "notes": data["notes"]
}

        books_collection.insert_one(book)
        return redirect(url_for("home"))
    return render_template("add_book.html")

@app.route("/update_book/<book_id>", methods=["GET", "POST"])
def update_book(book_id):
    book = books_collection.find_one({"book_id": book_id})

    if request.method == "POST":
        data = request.form
        updated_fields = {}
        
        if "status" in data:
            updated_fields["status"] = data["status"]
        if "current_page" in data:
            updated_fields["current_page"] = int(data["current_page"])
        if "notes" in data:
            updated_fields["notes"] = data["notes"]
        
        books_collection.update_one({"book_id": book_id}, {"$set": updated_fields})
        return redirect(url_for("home"))

    return render_template("update_book.html", book=book)

@app.route("/books/<user_id>")
def get_books(user_id):
    books = list(books_collection.find({"user_id": user_id}, {"_id": 0}))
    return render_template("books.html", books=books)

@app.route("/remove_book/<book_id>", methods=["GET", "POST"])
def remove_book(book_id):
    books_collection.delete_one({"book_id": book_id})
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)