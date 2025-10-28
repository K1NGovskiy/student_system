# Student Performance Management System

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success?logo=fastapi)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green?logo=mongodb)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap_5-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Modern web system for managing student academic performance**, built with **FastAPI**, **MongoDB**, and **Bootstrap 5**.  
> Designed for convenient storage, processing, and visualization of student data, grades, and analytics.

---

## Features

**FastAPI Backend** — lightweight REST API with automatic Swagger documentation  
**MongoDB 4.4** — flexible document-based database  
**Frontend:** HTML5 + CSS3 + Bootstrap 5 + JavaScript (ES6)  
**Dynamic data loading** through REST API  
**Data validation & error handling** via Pydantic  
**Modular design** — clean separation of backend and frontend  
**Average score analysis** and **performance summary** per group




---

## Installation

### 1️Clone repository
```bash
git clone https://github.com/K1NGovskiy/student_system.git
cd student_system
2️Install dependencies
Make sure you have Python 3.10+ and MongoDB 4.4+ installed.
pip install fastapi uvicorn pymongo pydantic
3️Run backend

python main.py
4️Run frontend
cd frontend
python -m http.server 8080
Then open in your browser:
http://localhost:8080/index.html

Automatic Startup
To simplify launch, use the included run_system.bat file.
run_system.bat
It will:

Start the FastAPI backend 

Run the local frontend server 

Automatically open the system in your browser 

Main Pages
Page	Description
index.html	Home dashboard with navigation
students.html	List of students with group filters
courses.html	Course and teacher management
grades.html	Gradebook with filters
summary.html	Summary of academic performance
average.html	Average grade per group

Technologies Used
Layer	Technologies
Backend	FastAPI, Pydantic, Uvicorn, PyMongo
Database	MongoDB 4.4
Frontend	HTML5, CSS3, JavaScript (ES6), Bootstrap 5, FontAwesome
Tools	Git, CMD, Browser, VS Code

API Documentation
Once the backend is running, open:
http://127.0.0.1:8000/docs

You’ll see the automatically generated Swagger UI with all API endpoints.



2025 — Course Project
