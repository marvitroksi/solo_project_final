from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.book import Book



@app.route('/show/<int:id>')
def showBook(id):
    if 'user' not in session:
        return redirect('/logout')

    data = {
        'book_id': id,
        'user_id': session['user']
    }
    info = Book.favUnfav(data)
    book = Book.getBookByID(data)
    favs = Book.getFavs(data)
    return render_template("showBook.html", book = book, favs = favs, info = info)

@app.route('/addBook')
def formToAdd():
    if 'user' not in session:
        return redirect('/logout')
    return render_template("createBook.html")

@app.route('/bookAdd', methods = ['POST'])
def addBook():
    if not Book.validate_book(request.form):
        flash("Please, fill in the fields correctly", 'BookCreate')
        return redirect(request.referrer)
    data = {
        'tittle': request.form['tittle'],
        'description': request.form['description'],
        'user_id': session['user']
    }
    Book.addBook(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def deleteBook(id): 
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'book_id': id
    }
    book = Book.getBookByID(data)
    if not session['user'] == book['user_id']:
        return render_template("404Error.html")
    print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    Book.deleteFaves(data)
    return redirect(request.referrer)

@app.route('/favorite/<int:id>')
def favorite(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'book_id': id,
        'user_id': session['user']
    }
    Book.favoriteBook(data)
    return redirect(request.referrer)

@app.route('/unfavorite/<int:id>')
def unfavorite(id):
    if 'user' not in session:
        return redirect('/logout')    
    data = {
        'book_id': id,
        'user_id': session['user']
    }
    Book.unfavoriteBook(data)
    return redirect(request.referrer)

@app.route('/editBook/<int:id>', methods = ['POST'])
def update(id):
    if not Book.validate_book(request.form):
        flash("Do not submit empty content", 'bookUpdate')
        return redirect(request.referrer)

    data = {
        'tittle': request.form['tittle'],
        'description': request.form['description'],
        'user_id' : session['user'],
        'book_id' : id

    }
    Book.updateBook(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def editForm(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'book_id' : id
    } 
    book = Book.getBookByID(data)
    if not session['user'] == book['user_id']:
        return render_template("404Error.html")
    return render_template('updateBook.html', book = Book.getBookByID(data))