from flask_app import app
from flask import render_template, request, redirect, session, flash, send_from_directory, send_file
from flask_app.models.book import Book
import os
# from contextlib import nullcontext
from datetime import datetime
import uuid as uuid
# Photo upload Imports
from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage

UPLOAD_FOLDER = 'flask_app/static/img/'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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
    file = request.files['files']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time += filename
        filename = time
        files = str(uuid.uuid1()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], files))
        data['files'] = files
    else:
        flash("Allowed files typse are .pdf, .txt", 'allowedError')
        return redirect(request.referrer)
    if request.files['files'] is None:
        files = ''
    if request.files['files'] is not None:
        files = request.files['files']
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

@app.route('/downloadPDF/<path:filename>')
def downloadPDF(filename):
    return send_file(app.root_path+'/static/img/'+filename, as_attachment=True)