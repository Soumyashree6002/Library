# Flask Authentication & Book Management App  

## Overview  
This is a Flask-based web application that provides user authentication and book management functionality. Users can register, log in, manage their accounts, and browse or add books based on their roles.  

## Features  
- **User Authentication**: Secure registration, login, and logout using JWT-based session management.  
- **Role-Based Access Control**:  
  - **Admin**: Can add books.  
  - **User**: Can browse books.  
- **Password Management**: Secure password hashing and reset functionality.  
- **Book Management**: Users can browse books with filters like genre, author, and rating.  

## Technologies Used  
- **Flask** – Web framework  
- **Flask SQLAlchemy** – ORM for database management  
- **Flask Bcrypt** – Secure password hashing  
- **Flask JWT Extended** – Authentication with JSON Web Tokens  
- **SQLite** – Default database (configurable)  

## API Endpoints  

### Authentication  
- **`POST /register`** – Register a new user  
- **`POST /login`** – Log in a user  
- **`GET /logout`** – Log out a user  
- **`POST /confirm`** – Confirm user identity before password reset  
- **`POST /forgot`** – Reset password  

### Book Management  
- **`POST /add_book`** – Add a new book (Admin only)  
- **`POST /add_another`** – Add another book (Admin only)  
- **`GET /books`** – Retrieve books with filters (pagination, genre, rating, author)  
- **`GET /books/<book_id>`** – Retrieve a specific book by ID  

