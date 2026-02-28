# 🍔 FoodExpress — Food Ordering Web App

A full-stack food ordering application built with **FastAPI, MySQL, HTML, CSS, and JavaScript**.

## 🚀 Features
- User Signup & Login (bcrypt password hashing)
- Browse restaurants & filter by cuisine
- Add to cart & place orders
- Personal dashboard with order history
- REST API with Swagger documentation

## 🛠 Tech Stack
- Frontend: HTML, CSS, Vanilla JS
- Backend: Python (FastAPI)
- Database: MySQL

## ⚙️ Run Locally
```bash
mysql -u root -p < schema.sql
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
