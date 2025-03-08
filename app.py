from flask import Flask, request, render_template, url_for, redirect, session, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import string
from datetime import timedelta
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies, decode_token

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", 'sqlite:///auth.db')
app.config['SQLALCHEMY_BINDS'] = {
    'books': os.getenv("BOOKS_DATABASE_URI", 'sqlite:///books.db')
}
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  
db = SQLAlchemy(app)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "your_jwt_secret") 
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_HTTPONLY'] = True
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
jwt = JWTManager(app)

@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return redirect(url_for('login')) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    ph_number = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique= True)
    is_admin = db.Column(db.Boolean, nullable = False)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name, ph_number, is_admin):
        self.name = name
        self.email = email
        self.ph_number = ph_number
        self.is_admin = is_admin
        self.password = bcrypt.generate_password_hash(password).decode('utf-8') 

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Book(db.Model):
    __bind_key__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable = False)
    genre = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.Float)

    def __init__(self, title, author, genre, rating):
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
    
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods= ['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        ph_number = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('pwd')
        is_admin = request.form.get('is_admin')
        
        if(is_admin == "on"):
            is_admin = True
        else:
            is_admin = False

        if(password != confirm_password):
            return render_template('register.html', error1 = "Passwords do not match. Please try again")

        existing_user = User.query.filter_by(email=email).first()
        if(existing_user):
            return render_template('register.html', error2 = "Account already exists with this email ID")
        
        existing_user = User.query.filter_by(ph_number=ph_number).first()
        if(existing_user):
            return render_template('register.html', error4 = "Account already exists with this phone number")
        
        has_alpha = any(c.isalpha() for c in password)  
        has_digit = any(c.isdigit() for c in password)  
        has_special = any(c in string.punctuation for c in password)

        strong_password = has_alpha and has_digit and has_special

        if(strong_password == False):
            return render_template('register.html', error3 = "Please enter a strong password(it should contain alphabets, numbers, as well as special characters)")

        new_user = User(email=email, password=password, name=name, ph_number=ph_number, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        
        access_token = create_access_token(identity=email, expires_delta=timedelta(hours=1))
        response = make_response(redirect(url_for('dashboard')))
        set_access_cookies(response, access_token)
        return response

    return render_template('register.html')

@app.route('/login', methods= ['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form['password']
        remember_me = request.form.get('remember')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            expires = timedelta(days=7) if remember_me else timedelta(hours=1)
            access_token = create_access_token(identity=email, expires_delta=expires)
            response = make_response(redirect(url_for('dashboard')))
            set_access_cookies(response, access_token)
            return response
        else:
            return render_template('login.html', error = 'Invalid email or password entered!')

    return render_template('login.html')

@app.route('/dashboard')
@jwt_required()
def dashboard():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if(user) :
        return render_template('dashboard.html', user=user)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    flash('Logout successful', 'success')
    return response

@app.route('/confirm', methods= ['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        email = request.form.get('email')
        ph_number = request.form.get('phone')

        user = User.query.filter_by(email= email).first()
        if(not user):
            return render_template('confirm.html', error = "No account exists with this email ID. Try again!")
        
        if user:
            if user.ph_number != ph_number:
                return render_template('confirm.html', error = "Email and phone number do not match. Please try again!")
            
            reset_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))

            return redirect(url_for('forgot', token=reset_token)) 


    return render_template('confirm.html')

@app.route('/forgot', methods = ['GET','POST'])
def forgot():
    token = request.args.get('token')

    if not token:
        flash("Invalid or expired reset link.", "danger")
        return redirect(url_for('confirm'))
    
    try:
        email = decode_token(token)['sub'] 
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('confirm'))

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('confirm'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('pwd')

        if(password != confirm_password):
            return render_template('forgot.html', error = "Passwords do not match. Please try again")
        
        has_alpha = any(c.isalpha() for c in password)  
        has_digit = any(c.isdigit() for c in password)  
        has_special = any(c in string.punctuation for c in password)

        strong_password = has_alpha and has_digit and has_special

        if(strong_password == False):
            return render_template('forgot.html', error = "Please enter a strong password(it should contain alphabets, numbers, as well as special characters)")    
        
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        flash("Password Changed Successfully!", "success")
        return redirect(url_for('login'))

    return render_template('forgot.html', token=token)

@app.route('/add_book', methods = ['GET','POST'])
@jwt_required()
def add_book():

    email = get_jwt_identity()  
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        rating = request.form.get('rating')

        if rating:
            rating = float(rating)
        else:
            rating = None

        new_book = Book(title = title, author = author, genre = genre, rating = rating)
        db.session.add(new_book)
        db.session.commit()
        flash("New book added successfully!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('add_book.html')

@app.route('/add_another', methods = ['GET', 'POST'])
@jwt_required()
def add_another():

    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        rating = request.form.get('rating')

        if rating:
            rating = float(rating)
        else:
            rating = None

        new_book = Book(title = title, author = author, genre = genre, rating = rating)
        db.session.add(new_book)
        db.session.commit()
        flash("New book added successfully!", "success")
    return redirect(url_for('add_book'))

@app.route('/books')
def books():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    genre = request.args.get('genre', None)
    rating = request.args.get('rating', None, type=float)
    author = request.args.get('author', None)

    books = Book.query

    if genre:
        books = books.filter(Book.genre.ilike(f"%{genre}%"))
    if rating:
        books = books.filter(Book.rating >= rating)
    if author:
        books = books.filter(Book.author.ilike(f"%{author}%"))

    if page and limit:
        books = books.paginate(page=page, per_page=limit, error_out=False)
        return jsonify({
            'total_books' : books.total,
            'current_page' : books.page,
            'total_pages': books.pages,
            'books' : [{'id' : b.id,
                        'title': b.title,
                        'author': b.author,
                        'genre': b.genre,
                        'rating': b.rating}
                        for b in books.items]
        })
    else:
        return jsonify([
            {'id' : b.id,
            'title': b.title,
            'author': b.author,
            'genre': b.genre,
            'rating': b.rating}
            for b in books.all()
        ])


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = Book.query.get(book_id) 
    if not book:
        return jsonify({'error': 'Book not found'}), 404  
    
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'rating': book.rating
    })


if __name__ == '__main__':
    app.run(debug=True)