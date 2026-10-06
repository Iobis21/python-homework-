from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)


# წიგნის დამატება
@app.route("/book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]

        book = Book(title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()
        return "წიგნი დაემატა!"

    return render_template("create_book.html", book=None)


# წიგნის რედაქტირება
@app.route("/update_book/<int:book_id>", methods=["GET", "POST"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return "წიგნი ვერ მოიძებნა", 404

    if request.method == "POST":
        book.title = request.form["title"]
        book.author = request.form["author"]
        book.year = request.form["year"]
        db.session.commit()
        return "წიგნი განახლდა!"

    return render_template("create_book.html", book=book)


# ერთი წიგნის ნახვა
@app.route("/get_book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return "წიგნი ვერ მოიძებნა", 404

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year
    })


# ყველა წიგნი
@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        })
    return jsonify(result)


# წიგნის წაშლა
@app.route("/delete_book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return "წიგნი ვერ მოიძებნა", 404

    db.session.delete(book)
    db.session.commit()
    return "წიგნი წაიშალა!"


if __name__ == "__main__":
    app.run(debug=True)
