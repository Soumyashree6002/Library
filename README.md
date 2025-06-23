# 📚 BookHive – Flask-Based Book Management Dashboard

## 🚀 Overview
**BookHive** is a full-stack web application to manage book collections with secure login, role-based access, and an elegant dashboard. Built with **Flask**, **Bootstrap 5**, and **JWT**, it offers a rich user experience with dark mode support, animations, and responsive card-based views.

<details>
<summary><strong>✨ Features</strong></summary>

### 🔐 Authentication & User Roles
- JWT-based secure authentication
- Role-based access:  
  - Admin → Add and manage books  
  - User → Browse and filter books

### 📚 Book Management
- Add/view books with title, author, genre, rating
- Filter by genre, rating, or limit
- Dynamic card rendering for an improved UX

### 🎨 UI/UX Upgrades
- Fully responsive dashboard with Bootstrap 5
- Light/Dark Mode toggle with CSS transitions
- Hero section with gradient background and animated text
- Modern card designs with hover effects

</details>

---

<details>
<summary><strong>🛠️ Tech Stack</strong></summary>

| Layer        | Technologies                               |
|--------------|--------------------------------------------|
| Backend      | Flask, Flask-JWT-Extended, SQLAlchemy      |
| Authentication | JWT, Flask-Bcrypt                       |
| Database     | SQLite (default)                           |
| Frontend     | HTML5, Bootstrap 5, Vanilla JS, Jinja2     |
| Styling      | Custom CSS, FontAwesome Icons              |

</details>

---

<details>
<summary><strong>📘 API Endpoints</strong></summary>

### 🔐 Authentication
- `POST /register` – Register a new user  
- `POST /login` – Login  
- `GET /logout` – Logout  
- `POST /confirm` – Confirm identity before password reset  
- `POST /forgot` – Reset password  

### 📚 Book Management
- `POST /add_book` – Add a book (Admin only)  
- `POST /add_another` – Add another book (Admin only)  
- `GET /books` – Fetch books (supports pagination + filters)  
- `GET /books/<book_id>` – Get a book by ID  

</details>

---

