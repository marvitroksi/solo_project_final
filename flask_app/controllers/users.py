from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.book import Book
from flask_app.models.user import User


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
    books = Book.getAllBooks(data)
    return render_template("userAccount.html", loggedUser = loggedUser, books = books)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')