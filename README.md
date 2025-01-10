# ExpenseOrbit

ExpenseOrbit is a comprehensive personal finance management system designed to help users efficiently track their transactions, set savings goals, and manage expenses. Built with FastAPI, SQLAlchemy, and PostgreSQL, it offers a robust and user-friendly interface for financial organization.

## Features

### User Management
- **Create Users**: Securely register users with hashed passwords.
- **Authentication**: Secure login using OAuth2.

### Transactions
- **Add Transactions**: Record income or expenses with categorized details.
- **View Transactions**: Retrieve all transactions for the current user.
- **Update Transactions**: Modify existing transaction details.
- **Delete Transactions**: Remove transactions securely.

### Categories
- **Create Categories**: Define custom categories for organizing transactions.
- **View Categories**: Retrieve all user-defined categories.
- **Delete Categories**: Remove unused categories.

### Savings Goals
- **Create Savings Goals**: Define target amounts and deadlines.
- **Track Progress**: Monitor savings progress dynamically based on transactions.
- **Mark Goals as Complete**: Complete and archive savings goals.

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Authentication**: OAuth2 with JWT Tokens
- **Deployment**: Docker, Nginx

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/expenseorbit.git
   cd expenseorbit
   ```

2. Set up a virtual environment and install dependencies:

   - **On Windows**:
     ```bash
     py -3 -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     ```

   - **On macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

3. Configure environment variables:
   - Create a `.env` file in the project root.
   - Add the following variables:
     ```env
     DATABASE_URL=postgresql://user:password@localhost/expenseorbit
     SECRET_KEY=your_secret_key
     ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API documentation:
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## API Endpoints

### User Management
- `POST /users/`: Register a new user.

### Transactions
- `POST /transactions/`: Add a new transaction.
- `GET /transactions/`: Retrieve all transactions.
- `PUT /transactions/{transaction_id}`: Update a transaction.
- `DELETE /transactions/{transaction_id}`: Delete a transaction.

### Categories
- `POST /categories/`: Create a new category.
- `GET /categories/`: Retrieve all categories.
- `DELETE /categories/{category_id}`: Delete a category.

### Savings Goals
- `POST /savings/`: Create a new savings goal.
- `GET /savings/`: Retrieve all savings goals.
- `PUT /savings/{goal_id}/complete`: Mark a savings goal as complete.

## Project Structure

```
expenseorbit/
├── app/
│   ├── auth/
│   ├── database.py
│   ├── models.py
│   ├── routers/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   ├── savings.py
│   │   └── auth.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   └── savings.py
│   └── utils/
│       └── hash.py
├── alembic/
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```


## Contact

For inquiries or support, contact:
- **Email**: your-email@example.com
- **GitHub**: [your-github-profile](https://github.com/your-profile)
