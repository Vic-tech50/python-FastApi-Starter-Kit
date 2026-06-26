# 🚀 FastAPI Boilerplate & Learning Project

A comprehensive **FastAPI Boilerplate** designed to accelerate backend development while serving as a complete learning resource for modern API development.

This project demonstrates production-ready implementation of authentication, authorization, CRUD operations, email notifications, OTP verification, payments, caching, middleware, WebSockets, scheduling, and many other backend concepts using **FastAPI**, **SQLAlchemy**, **MySQL**, and **Jinja2**.

---

# 📌 Project Goals

The primary goals of this project are to:

* Learn FastAPI from beginner to advanced level.
* Build a reusable backend boilerplate.
* Reduce development time for future projects.
* Demonstrate production-ready backend architecture.
* Serve as a reference project for future FastAPI applications.

---

# 🛠 Tech Stack

* FastAPI
* Python 3
* SQLAlchemy ORM
* MySQL
* Jinja2 Templates
* HTML
* CSS
* JavaScript
* Session Authentication
* JWT Authentication
* OAuth (Google & GitHub)
* APScheduler
* WebSockets
* SMTP Email
* HTTPX
* Passlib (Password Hashing)
* Python-dotenv
* Pydantic
* Uvicorn

---

# 📁 Project Structure

```
project/
│
├── main.py
├── database.py
├── models.py
├── config/
│   ├── oauth.py
│   └── settings.py
│
├── routes/
│   ├── auth.py
│   ├── home.py
│   ├── blog.py
│   ├── websocket.py
│   └── payment.py
│
├── templates/
│
├── static/
│
├── uploads/
│
├── cron/
│
├── services/
│
└── requirements.txt
```

---

# ✅ Features Implemented

## Authentication

* User Registration
* User Login
* Logout
* Password Hashing
* Session Authentication
* JWT Authentication
* Multi Authentication
* Role-Based Authentication
* Protected Routes
* Middleware Authorization

---

## Roles

* Admin
* Manager
* User

Each role has its own dashboard and route protection.

---

## CRUD Operations

Implemented complete CRUD functionality with:

* Create
* Read
* Update
* Delete

Including:

* Validation
* Image Upload
* Flash Messages
* Redirects
* Old Input Handling

---

## File Upload

Supports:

* Images
* Profile Pictures
* Blog Images

Features:

* UUID File Names
* Upload Directory
* Validation
* Database Storage

---

## Form Validation

Validation includes:

* Required Fields
* Email Validation
* Password Validation
* Number Validation
* String Validation
* Length Validation
* Duplicate Email Check

---

## Sessions

Implemented session-based authentication.

Used for:

* Login State
* Flash Messages
* Success Messages
* Error Messages
* OTP
* User Information

---

## JWT

Implemented JWT Authentication with:

* Login
* Token Creation
* Token Verification
* Protected Routes

---

## Password Reset

Implemented:

* Forgot Password
* Email Reset Link
* Password Update

---

## OTP Verification

Features:

* Generate OTP
* Email OTP
* OTP Expiration
* Database Storage
* Verification
* Secure Validation

---

## Email Notifications

SMTP Email Integration

Supports:

* Registration Emails
* Contact Messages
* OTP Emails
* Password Reset
* HTML Email Templates
* Background Tasks

---

## OAuth Authentication

Implemented Social Login using:

* Google OAuth
* GitHub OAuth

Future Support:

* Facebook
* Microsoft
* LinkedIn

---

## Middleware

Implemented:

* Session Middleware
* Authentication Middleware
* Authorization Middleware
* Logging Middleware
* Rate Limiting Concepts

---

## Caching

Implemented examples using:

* Memory Cache
* Session Cache

Covered:

* Cache Hit
* Cache Miss
* Cache Expiration

---

## SQLAlchemy

Covered:

* Models
* Relationships
* CRUD
* Sessions
* Transactions
* Query Builder
* Lazy Loading
* Eager Loading
* ORM Concepts

---

## WebSockets

Implemented real-time communication.

Examples:

* Chat System
* Live Notifications
* Online Users
* Broadcast Messages

---

## HTTP Client

Using HTTPX

Covered:

* GET
* POST
* PUT
* DELETE
* External APIs
* Mock APIs
* API Services

---

## Cron Jobs

Implemented scheduled tasks using APScheduler.

Examples:

* OTP Cleanup
* Email Scheduler
* Automatic Tasks

---

## Payments

Implemented payment integrations:

* Paystack
* Flutterwave
* Stripe

Topics covered:

* Payment Initialization
* Payment Verification
* Callback URLs
* Secure Payment Flow

---

## Security

Implemented:

* Password Hashing
* JWT
* Sessions
* OTP
* OAuth
* Route Protection
* Authentication Middleware
* Authorization
* Login Attempt Limiting
* Account Locking

---

## Error Handling

Covered:

* HTTPException
* Validation Errors
* Database Errors
* Authentication Errors
* Custom Error Messages

---

## Environment Variables

Using `.env`

Examples:

* Database Credentials
* Mail Credentials
* OAuth Keys
* JWT Secret
* API Keys

---

# 📚 Concepts Learned

## FastAPI

* Routing
* Dependencies
* APIRouter
* Request
* Response
* RedirectResponse
* Form
* File Upload
* UploadFile
* Background Tasks
* Middleware
* Sessions
* WebSockets
* Dependency Injection

---

## SQLAlchemy

* Base Models
* ORM
* Relationships
* Queries
* Filtering
* Ordering
* Transactions

---

## Authentication

* Sessions
* JWT
* OAuth
* Multi Authentication
* Role-Based Authentication

---

## API Development

* REST APIs
* HTTP Methods
* CRUD
* Validation
* External APIs

---

## Security

* Password Hashing
* OTP
* Login Protection
* Authorization

---

## Notifications

* Email
* OTP
* Background Tasks

---

## Realtime

* WebSockets
* Live Chat
* Notifications

---



# 🎯 Purpose

This repository is intended to become a complete reference for building modern FastAPI applications, demonstrating both fundamental and advanced backend concepts through practical, production-oriented examples.

It is suitable for developers learning FastAPI as well as those looking for a reusable backend starter project.

---

# ⭐ Contributions

Contributions, issues, and feature requests are welcome.

Feel free to fork this repository, open pull requests, or suggest improvements.

---

# 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Victor Okenyi**

Full Stack Developer

Backend • FastAPI • Laravel • React • React Native • Next.js • Electron.js • SQL • API Development
