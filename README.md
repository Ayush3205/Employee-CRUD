# Employee Management API

A FastAPI-based Employee Management System with MongoDB database that provides comprehensive CRUD operations, aggregation queries, and search functionality for employee data.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete employees
- **Department Filtering**: List employees by department with sorting
- **Salary Aggregation**: Calculate average salary by department using MongoDB aggregation
- **Skill Search**: Search employees by specific skills
- **Pagination Support**: Built-in pagination for large datasets
- **Data Validation**: Comprehensive input validation using Pydantic
- **Async Operations**: Asynchronous database operations for better performance
- **Interactive Documentation**: Auto-generated API documentation with Swagger UI

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.8+** (Python 3.11 or 3.12 recommended for better compatibility)
- **MongoDB Community Server**
- **Git** (optional, for cloning)

## 🛠 Installation & Setup

### Step 1: Clone or Download the Project

```bash
# Option 1: Clone the repository (if using Git)
git clone <repository-url>
cd employee-management-api

# Option 2: Create project directory manually
mkdir employee-management-api
cd employee-management-api
```

### Step 2: Create Project Structure

Create the following directory structure:

```
employee-management-api/
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
└── routers/
    └── employees.py
```

### Step 3: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv
```

### Step 4: Install Dependencies

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### Step 5: MongoDB Setup

## 🚀 Run the Application

```bash
# Start the FastAPI server
uvicorn main:app --reload
```

The server will start at: **http://localhost:8000**

### Access Points:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000
