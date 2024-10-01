# Transacto

**Transacto** is a banking transaction system built using Django, providing functionality to manage users, accounts, and transactions with support for multi-currency transfers.

## Features
- User registration and authentication
- Account management with balance tracking
- Multi-currency transaction support using exchange rates fetched from a live API
- Logging of both deposit and withdrawal transactions
- Integration with a third-party exchange rate API

## Prerequisites
Before running this project locally, make sure you have the following installed:
- **Python 3.8+**
- **PostgreSQL** (or another database if configured)
- **pip** (Python package installer)
- **Virtualenv** (optional but recommended)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [repository]
cd transacto
```

### 2. Create Virrtual Enviorment 
```bash
python3 -m venv env 
source env/bin/activate 
```

### 3. Install Project Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
EXCHANGE_API_KEY=your_exchange_api_key
```

### 5. Set Up the Database
```bash
python manage.py makemigrations
python manage.py migrate
```
