from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.book import Book
from flask_app.models.user import User
import urllib.request
import os
from werkzeug.utils import secure_filename
import uuid as uuid

UPLOAD_FOLDER = 'flask_app/static/img/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addProfilePic', methods = ['GET','POST'])
def uploadPhoto():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    file = request.files['profile_pic']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        profile_pic = str(uuid.uuid1()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
        data['profile_pic'] = profile_pic
    else:
        flash("Allowed image types are .png, .jpg, .jpeg", 'allowedError')
        return redirect(request.referrer)

    User.updateUserPhoto(data)
    return redirect(request.referrer)


@app.route('/')
def index():
    return render_template("loginRegistration.html")

@app.route('/register', methods = ['POST'])
def registerUser():
    if not User.validate_user(request.form):
        flash("Fill the fields correctly.", 'signUp')
        return redirect(request.referrer)
    if User.getUserByEmail(request.form):
        flash("This email already exists, try another one.", 'emailRegister')
        return redirect(request.referrer)
    
    data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    User.addUser(data)
    flash("You are ready to login", 'signUpSuccess')
    return redirect(request.referrer)

@app.route('/login', methods = ['POST'])
def loginUser():
    data = {
        'email' : request.form['email'],
        'password': request.form['password']
    }
    if len(request.form['email'])< 1:
        flash("Email is required to login.", 'emailLogin')
        return redirect(request.referrer)
    if not User.getUserByEmail(data):
        flash("This email doesn't exits.", 'emailLogin')
        return redirect(request.referrer)
    user = User.getUserByEmail(data)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect password", 'passwordLogin')
        return redirect(request.referrer)
    
    session['user'] = user['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    
    loggedUser = User.getUserByID(data)
    favs = Book.favUnfav(data)
    books = Book.getAllBooks(data)
    user = User.getUsersBooks(data)
    return render_template("dashboard.html", loggedUser = loggedUser, books = books, user = user, favs = favs)


@app.route('/account')
def userAccount():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    } 
    loggedUser = User.getUserByID(data)
    books = User.getUsersBooks(data)
    favs = User.getUsersFavorites(data)
    return render_template("userprofile.html", loggedUser = loggedUser, books = books, favs = favs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/updateUser', methods = ['POST'])
def updateUser():
    if not User.validate_updated_user(request.form):
        flash("Please enter the fields carefully", 'updateError')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'user_id': session['user']
    }
    User.updateUser(data)
    return redirect(request.referrer)