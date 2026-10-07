# 🏦 Code Legion Bank

<p align="center">
  <strong>A modular Python banking system built from the ground up.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Testing-pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/Status-Complete-2EA44F?style=for-the-badge" alt="Project Status">
</p>

<p align="center">
  <em>A practical Python project focused on OOP, authentication, database persistence, session management, modular design, banking operations, and automated testing.</em>
</p>

---

## 📑 Table of Contents

* [🎯 About the Project](#-about-the-project)
* [✨ Features](#-features)
* [🏗️ How the System Works](#️-how-the-system-works)
* [🧩 Project Architecture](#-project-architecture)
* [📦 Modules](#-modules)
* [💾 Database and Data Persistence](#-database-and-data-persistence)
* [🔐 Security](#-security)
* [💰 Account Balance Handling](#-account-balance-handling)
* [🚀 Getting Started](#-getting-started)
* [▶️ Running the Application](#️-running-the-application)
* [🧪 Running the Tests](#-running-the-tests)
* [📂 Project Structure](#-project-structure)
* [🧠 Learning Notes](#-learning-notes)
* [✅ Project Status](#-project-status)
* [🔮 Future Improvements](#-future-improvements)
* [⚠️ Disclaimer](#️-disclaimer)

---

## 🎯 About the Project

**Code Legion Bank** is a console-based banking application developed in Python as a practical software-development project.

The project started from the idea of building a simple banking/ATM program and gradually evolved into a more structured banking system using:

* Object-Oriented Programming
* Modular Python design
* Authentication
* Password and PIN hashing
* Database persistence
* Session management
* Banking operations
* Input validation
* Automated testing

Rather than keeping the entire application inside one large Python file, the system was separated into modules with specific responsibilities.

The result is a small but complete banking simulation where customers can create profiles, create bank accounts, authenticate themselves, perform transactions, and view their transaction history.

---

## ✨ Features

| Feature                  | Description                                                     |
| ------------------------ | --------------------------------------------------------------- |
| 👤 Customer Registration | Create a new customer profile                                   |
| 🔑 Customer Login        | Authenticate using Customer ID and password                     |
| 🏦 Multiple Accounts     | Customers can create and select bank accounts                   |
| 💳 Account Types         | Supports Savings and Current accounts                           |
| 💰 Deposits              | Deposit funds into the active account                           |
| 💸 Withdrawals           | Withdraw funds after PIN verification                           |
| 🔄 Transfers             | Transfer funds between bank accounts                            |
| 📜 Transaction History   | View recorded account transactions                              |
| 📧 Email Updates         | Change the customer's registered email                          |
| 📱 Phone Updates         | Change the customer's registered phone number                   |
| 🔐 Password Security     | Passwords are hashed before storage                             |
| 🔢 PIN Security          | Account PINs are hashed before storage                          |
| 👥 Session Management    | Tracks the active customer and account                          |
| 🧪 Automated Testing     | Functionality tested using pytest                               |
| 💾 Database Persistence  | Customer, account, and transaction data are stored persistently |

---

## 🏗️ How the System Works

The application follows a layered user workflow:

```text
                         🏦 CODE LEGION BANK
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Main Menu    │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
             👤 Register                    🔑 Login
                                                │
                                                ▼
                                      ┌──────────────────┐
                                      │ Customer Session │
                                      └────────┬─────────┘
                                               │
                                               ▼
                                      👤 Customer Dashboard
                                               │
                  ┌───────────────┬────────────┼───────────────┐
                  ▼               ▼            ▼               ▼
             🏦 Accounts       🆕 Create    📧 Update       📱 Update
                  │             Account      Email           Phone
                  │
                  ▼
          🎯 Active Account
                  │
                  ▼
        ┌─────────────────────┐
        │ Account Operations  │
        └──────────┬──────────┘
                   │
        ┌──────────┼──────────┬───────────────┐
        ▼          ▼          ▼               ▼
      💰 Deposit  💸 Withdraw 🔄 Transfer   📜 History
```

This separation allows the program to move from the unauthenticated main system into an authenticated customer session and finally into operations on a selected bank account.

---

## 🧩 Project Architecture

The application is divided into separate modules.

```text
                         main.py
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
      authentication    session        workflows
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                  Customer / Account
                     Objects
                            │
                            ▼
                banking_operations.py
                            │
                            ▼
                     database.py
                            │
                            ▼
                       SQLite DB
```

### Design idea

The important idea is that **different responsibilities live in different places**.

For example:

```text
authentication.py
        ↓
"Is this password/PIN correct?"

account.py
        ↓
"What is this account's current in-memory state?"

banking_operations.py
        ↓
"Perform the banking operation and persist the change."

database.py
        ↓
"How do we communicate with the database?"

session.py
        ↓
"Who is currently logged in and which account is active?"
```

This makes the system easier to test, debug, maintain, and extend.

---

## 📦 Modules

| Module                  | Responsibility                                            |
| ----------------------- | --------------------------------------------------------- |
| `main.py`               | Main application workflows and user interface             |
| `authentication.py`     | Password and PIN hashing/verification                     |
| `banking_operations.py` | Deposit, withdrawal and transfer operations               |
| `database.py`           | Database creation, queries and persistent data operations |
| `customer.py`           | Customer object and customer-related behaviour            |
| `account.py`            | Account object and in-memory account behaviour            |
| `session.py`            | Active customer/account session state                     |
| `utilities.py`          | ID, account number and timestamp generation               |

### `main.py`

Acts as the main application controller.

It contains workflows for:

* Main menu
* Customer registration
* Customer login
* Customer dashboard
* Account selection
* Account creation
* Deposits
* Withdrawals
* Transfers
* Transaction history
* Customer information updates
* Logout

### `authentication.py`

Responsible for security-related authentication functions.

It handles:

* Password hashing
* Password verification
* PIN hashing
* PIN verification

### `banking_operations.py`

Contains the actual banking operations that interact with persistent account data.

Examples include:

```text
Deposit
Withdrawal
Transfer
```

### `database.py`

Acts as the application's database layer.

It handles tasks such as:

* Database initialisation
* Customer storage
* Customer lookup
* Account storage
* Account lookup
* Customer account retrieval
* Customer information updates
* Transaction retrieval
* Transaction persistence

### `customer.py`

Contains the `Customer` object.

The object represents the currently loaded customer's information during program execution.

### `account.py`

Contains the `Account` object.

The account object represents the account currently loaded into the application and provides methods for updating its in-memory state.

### `session.py`

Controls the currently active session.

The session is responsible for keeping track of things such as:

```text
Active Customer
       │
       ▼
Active Account
       │
       ▼
Current Session
```

It also provides methods for starting and clearing a session.

### `utilities.py`

Contains reusable helper functions such as:

* Customer ID generation
* Account number generation
* Timestamp generation

---

## 💾 Database and Data Persistence

The project uses a database to persist important banking information.

The database stores information relating to:

### 👤 Customers

```text
Customer ID
Name
Email
Phone Number
Date of Birth
Password Hash
```

### 🏦 Accounts

```text
Account Number
Account Label
Account Type
Account Balance
Account PIN Hash
Customer ID
Account Creation Date
```

### 📜 Transactions

```text
Transaction ID
Account Number
Transaction Type
Transaction Amount
Balance Before
Balance After
Transaction Date
```

This allows information to remain available after the Python program is closed and started again.

---

## 🔐 Security

Security was considered throughout the implementation.

### 🔑 Password Hashing

Customer passwords are hashed before being stored.

The application does not need to store the original password in plain text.

During login:

```text
Entered Password
       │
       ▼
Password Verification
       │
       ▼
Stored Password Hash
       │
       ▼
Authenticated / Rejected
```

### 🔢 Account PIN Hashing

Account PINs follow the same general principle.

The four-digit PIN entered by the customer is hashed before storage and later verified against the stored hash.

### 🚫 Attempt Limits

Authentication-sensitive operations have limited attempts.

For example:

```text
Customer Login
     └── Password attempts

Withdrawal
     └── Account PIN attempts

Transfer
     └── Account PIN attempts
```

### 🛡️ Additional Validation

The system also validates things such as:

* Empty input
* Invalid numeric input
* Invalid account selection
* Invalid account PIN
* Insufficient funds
* Invalid deposit amount
* Invalid withdrawal amount
* Invalid transfer amount
* Transfers to the same account

---

## 💰 Account Balance Handling

One important design decision in the project is the difference between **persistent database state** and **active in-memory object state**.

When a banking operation is performed, the operation module handles the database-side change.

At the same time, the currently active `Account` object needs to reflect the new balance immediately.

For example:

```text
User deposits GHC 50.00
          │
          ▼
banking_operations.py
          │
          ├──────────► Database balance updated
          │
          ▼
Active Account object
          │
          ▼
In-memory balance updated
```

This means the user does not have to log out and log back in simply to see a balance that was changed during the current session.

The account object's normal methods are therefore useful for **temporary in-memory state management**, while the banking operations module is responsible for the persistent database operation.

This separation was important during development because an earlier implementation could update the database while the already-loaded account object still contained its previous balance.

---

## 🚀 Getting Started

### Requirements

You need:

* Python 3.10+
* `pytest` for running the automated tests
* A terminal
* The project source code

No external banking service is required.

### Clone the repository

```bash
git clone https://github.com/healerXcuppa/code-legion-phantom.git
cd Projects/'Bank System'
```

### Install pytest

If pytest is not already installed:

```bash
python -m pip install pytest
```

---

## ▶️ Running the Application

Start the application with:

```bash
python main.py
```

The program first initialises the database and then launches the main banking menu.

You will be presented with options similar to:

```text
[1]. Login to Existing Customer Account
[2]. Register New Customer Profile
[3]. Exit Application
```

From there, the user can navigate through the customer and account workflows.

---

## 🧪 Running the Tests

The project uses **pytest** for automated testing.

Run:

```bash
pytest tests/
```

For more detailed output:

```bash
pytest -v
```

The project went through multiple testing cycles during development.

When problems were discovered, they were investigated, corrected, and tested again.

The final implementation passed the completed test suite successfully.

> **Testing status: ✅ Passed**

---

## 📂 Project Structure

The core project follows a modular structure similar to:

```text
Code-Legion-Bank/
│
├── main.py
├── authentication.py
├── banking_operations.py
├── database.py
├── customer.py
├── account.py
├── session.py
├── utilities.py
│
├── tests/
│   ├── test_modules.py
│   └── full_automated_test.py
│
├── NOTES.md
├── README.md
└── .gitignore
```

> The exact contents of the `tests/` directory depend on the final test files in the repository.

---

## 🧠 Learning Notes

This project was not only about producing a working banking application.

It was also a major learning project.

During development, different Python concepts and software-development practices were studied and applied directly to the system.

The notes document things learned during the project, implementation decisions, problems encountered, and lessons from building and testing the application.

📖 **[Read the project learning notes →](NOTES.md)**

---

## ✅ Project Status

### Implementation

**Complete**

The major application workflows have been implemented.

### Testing

**Complete**

The project was tested using pytest, and issues discovered during testing were corrected and retested.

### Core functionality

| Area                    | Status |
| ----------------------- | :----: |
| Customer registration   |    ✅   |
| Customer authentication |    ✅   |
| Session management      |    ✅   |
| Account creation        |    ✅   |
| Account selection       |    ✅   |
| Deposits                |    ✅   |
| Withdrawals             |    ✅   |
| Transfers               |    ✅   |
| Transaction history     |    ✅   |
| Email updates           |    ✅   |
| Phone updates           |    ✅   |
| Password hashing        |    ✅   |
| PIN hashing             |    ✅   |
| Automated testing       |    ✅   |

### Overall

> 🟢 **PROJECT IMPLEMENTATION AND TESTING COMPLETE**

---

## 🔮 Future Improvements

Although the current project implementation is complete, the system could be expanded in the future.

Possible directions include:

* 🖥️ Graphical user interface
* 🌐 Web-based banking interface
* 👨‍💼 Administrative dashboard
* 📊 Improved reporting
* 🧾 More advanced transaction records
* 🔒 Additional security mechanisms
* 🧪 Expanded test coverage
* ⚙️ Improved configuration management
* 🏦 Additional banking features

These are future possibilities rather than unfinished requirements of the current implementation.

---

## ⚠️ Disclaimer

> **Code Legion Bank is an educational banking simulation.**

This project is intended for learning and software-development practice.

It should **not** be used to handle real customer funds, real banking credentials, or production financial transactions.

---

## 🧑‍💻 Project Journey

This project began as a smaller banking/ATM-style Python exercise and gradually grew into a more structured application.

The development process involved learning and applying:

```text
Python Fundamentals
        ↓
Functions
        ↓
Object-Oriented Programming
        ↓
Encapsulation
        ↓
Modular Design
        ↓
Authentication
        ↓
Database Operations
        ↓
Session Management
        ↓
Banking Workflows
        ↓
Automated Testing
        ↓
Debugging & Refinement
        ↓
✅ Completed Project
```

The final system represents the practical application of the concepts learned throughout the project.

---

<p align="center">
  <strong>🏦 Code Legion Bank</strong>
  <br>
  <em>Built to learn. Built to test. Built to understand.</em>
</p>
