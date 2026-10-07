# 🧠 CODE LEGION BANK — PROJECT LEARNING NOTES

> These are some of the things I learnt, understood better, and used while building the Code Legion Bank project.
>
> I wrote these notes mainly for myself so that if I come back to this project later, I can remember **why I did certain things**, not just what the code does.

---

## 📌 Table of Contents

* [Context Managers](#-context-managers)
* [Instantiation and `__init__()`](#️-instantiation-and-__init__)
* [Python `secrets` Module](#-python-secrets-module)
* [Hashing, Salting and `hashlib`](#-hashing-salting-and-hashlib)
* [Encryption vs Hashing](#-encryption-vs-hashing)
* [Python `datetime` Library](#-python-datetime-library)
* [Database ACID Properties](#️-database-acid-properties)
* [Objects, Classes and In-Memory State](#-objects-classes-and-in-memory-state)
* [Database Persistence vs Temporary Object Updates](#-database-persistence-vs-temporary-object-updates)
* [Functions, Parameters and Arguments](#-functions-parameters-and-arguments)
* [`return` vs `print`](#-return-vs-print)
* [PIN Verification and Indexing](#-pin-verification-and-indexing)
* [Working With Money](#-working-with-money)
* [Session Management](#-session-management)
* [Testing With Pytest](#-testing-with-pytest)
* [What I Finally Learnt From The Project](#-what-i-finally-learnt-from-the-project)

---

# 🧩 Context Managers

A context manager is basically a Python mechanism that helps manage resources or actions properly before, during and after a block of code runs.

The main thing I learnt here is the `with` statement.

A context manager normally works through:

```python
__enter__()
__exit__()
```

The `__enter__()` method is used when entering the context, while `__exit__()` is automatically called when leaving it.

The important part for me was understanding that `__exit__()` can also deal with exceptions.

If an exception happens inside the `with` block:

* returning `False` or another false value means the exception is **not swallowed**, so Python continues propagating it and I can still get the traceback.
* returning `True` means the context manager is saying that the exception has been handled and Python can continue after the `with` block.

So basically:

```text
__exit__() → False → exception continues
__exit__() → True  → exception is suppressed
```

This made me understand why context managers can be useful when working with resources such as files or database connections.

Python's `with` statement guarantees that `__exit__()` is called after entering the context successfully, even when the body raises an exception.

### `finally`

I also learnt about `finally`.

`finally` is useful when I want Python to perform something **regardless of whether the operation succeeded or an exception occurred**.

For example:

```python
try:
    # do something
except Exception:
    # handle error
finally:
    # this should still happen
```

The important thing I understood is that `finally` does not magically execute if Python never reaches that part of the program in the first place. It works as part of the exception-handling flow once execution has entered the `try` statement.

---

# 🏗️ Instantiation and `__init__()`

Instantiation was one of the things I had to understand better when working with my account and customer objects.

When I create an object from a class, I am basically creating an **instance of that class**.

For example:

```python
account = Account(...)
```

The `Account` class is the blueprint while `account` is the actual object created from that blueprint.

The `__init__()` method is automatically called when the object is created and is normally used to initialise the object's instance variables.

For example:

```python
class Account:

    def __init__(self, account_number, account_balance):
        self.account_number = account_number
        self.account_balance = account_balance
```

Then:

```python
account = Account("ACC-12345", 50000)
```

creates an Account object and gives that object its own values.

One thing I finally understood properly is:

```text
Class = blueprint
Object = actual thing created from the blueprint
Instantiation = creating that object
__init__() = initial setup of the object
```

This became very important in the bank project because I had separate objects for things like customers and accounts.

---

# 🔐 Python `secrets` Module

The Python `secrets` module is a library designed for generating **cryptographically strong random values**.

I used it in the project because normal random generation is not what I want when generating values connected to security.

One method I used was:

```python
secrets.choice(...)
```

This lets Python securely choose one item from a sequence.

I used this concept when generating account numbers.

One thing I initially misunderstood was thinking that `choice()` automatically makes every choice unique. It doesn't.

If I need uniqueness, I still need to check whether the generated value already exists.

---

## `token_hex()`

Another method I learnt about is:

```python
secrets.token_hex()
```

This generates random bytes and represents them as hexadecimal characters.

For example:

```python
secrets.token_hex(8)
```

means Python generates **8 random bytes** and converts them into hexadecimal.

Because every byte becomes two hexadecimal characters, 8 bytes produces:

```text
16 hexadecimal characters
```

That gives:

```text
8 × 8 = 64 bits
```

of randomness.

So `token_hex(8)` is not 8 hexadecimal bytes. It is **8 random bytes represented using 16 hexadecimal characters**.

This helped me understand the difference between:

```text
bytes
bits
hexadecimal representation
```

---

# 🔑 Hashing, Salting and `hashlib`

This was probably one of the more important security topics I learnt during the project.

Before talking about `hashlib`, I had to understand the difference between **encryption and hashing**.

---

# 🔒 Encryption vs Hashing

### Encryption

Encryption is designed to transform readable information into unreadable information using a cryptographic process, with the intention that the original information can later be recovered using the appropriate key.

Basically:

```text
Original data
     ↓
Encryption
     ↓
Encrypted data
     ↓
Decryption
     ↓
Original data
```

### Hashing

Hashing works differently.

A cryptographic hash is designed to produce a value from the original input that is not meant to be reversed back into the original value.

So for passwords, the application should not need to store the actual password.

Instead:

```text
Password
   ↓
Password hashing
   ↓
Stored derived value
```

When the user logs in:

```text
Entered password
       ↓
Same password-hashing process
       ↓
Compare with stored value
```

This is why passwords should not simply be encrypted and stored like normal data.

---

# 🧂 Salts

I also learnt why simply hashing passwords is not enough.

If two users have the same password and the same hashing process is used without a salt, they can end up with the same hash.

That creates problems because attackers can use precomputed tables, such as rainbow tables, to help identify common password hashes.

A **salt** is random data added into the password-derived process so that the same password can produce different stored results.

In my authentication module, I used:

```python
secrets.token_bytes(...)
```

to generate random salt bytes.

Python's documentation recommends a proper random source and notes that salts for password-based derivation should generally be around 16 bytes or more.

---

# 🧪 `hashlib.pbkdf2_hmac()`

The project also introduced me to:

```python
hashlib.pbkdf2_hmac()
```

PBKDF2 is a password-based key derivation function.

Instead of doing something simple like:

```python
sha256(password)
```

PBKDF2 performs the derivation repeatedly using an iteration count, making brute-force attacks more expensive.

The process I learnt was roughly:

```text
Password
   +
Random Salt
   ↓
PBKDF2-HMAC
   ↓
Derived hash
   ↓
Store salt + derived value
```

The salt doesn't need to be secret. Its purpose is to make each password derivation unique.

I also learnt that the result from `pbkdf2_hmac()` is returned as bytes. If I want to store it as hexadecimal text, I can use:

```python
derived_key.hex()
```

and later convert it back using:

```python
bytes.fromhex(value)
```

This helped me understand the difference between the **actual bytes** and their **text representation**.

---

# 🕒 Python `datetime` Library

The `datetime` library helped me work with dates and times in the banking system.

I used it for things such as:

* account creation dates
* transaction timestamps
* customer date of birth
* recording when banking operations occurred

I also learnt about ISO-style date/time formatting.

One important correction to my original understanding is that Python's `datetime` module does **not automatically know the physical location of the user and convert everything to their local timezone**.

If I explicitly use UTC, then I am working with UTC time.

The idea is basically:

```text
System/application time
       ↓
datetime
       ↓
standardised timestamp
       ↓
database transaction record
```

Using a standard timestamp is important in something like a bank system because transaction records need consistent time information.

---

# 🗄️ Database ACID Properties

ACID was another concept I learnt while working with the database.

ACID is used to describe properties that help database transactions remain reliable.

## A — Atomicity

Atomicity means a transaction should happen as **one complete unit**.

Either:

```text
Everything succeeds
```

or:

```text
Everything fails / rolls back
```

For example, during a transfer:

```text
Remove GHC 100 from Account A
+
Add GHC 100 to Account B
```

I don't want the first operation to succeed while the second one fails.

That would create an inconsistent banking system.

---

## C — Consistency

Consistency means the database should move from one valid state to another valid state while maintaining its rules and constraints.

For example, if the database says an account balance cannot become invalid, a transaction should not leave it in an invalid state.

---

## I — Isolation

Isolation means transactions should not interfere with each other in a way that produces incorrect results.

This becomes especially important when multiple users or transactions are happening at the same time.

---

## D — Durability

Durability means that once a transaction has successfully been committed, the change should remain saved even if something happens afterward, such as a system restart or power failure.

So basically:

```text
Atomicity   → All or nothing
Consistency → Valid state → valid state
Isolation   → Transactions don't interfere incorrectly
Durability  → Saved means saved
```

This made me understand that databases are not just about storing information. They also need rules that protect the reliability of that information.

---

# 🧱 Objects, Classes and In-Memory State

One of the biggest things I learnt from this project was that an object existing in Python memory and data existing in the database are **not automatically the same thing**.

For example, I can have:

```python
active_account
```

as an Account object currently being used by the program.

That object can contain:

```text
balance = GHC 500
```

while the database may contain another stored value.

If I change the object:

```python
active_account.deposit(amount)
```

I am changing the object currently in memory.

That does not automatically mean the database has been changed.

This distinction became very important when I was handling deposits and withdrawals.

---

# 💾 Database Persistence vs Temporary Object Updates

I originally had an issue where the banking operation updated the database, but the currently active Account object didn't immediately reflect the new balance.

For example:

```text
Database balance → updated
Account object    → old balance
```

So the program could still display the old balance until the account was retrieved from the database again.

I solved this by deliberately handling both sides where appropriate:

```python
ops.deposit(...)
```

updates the persistent database state.

Then:

```python
active_account.deposit(...)
```

updates the Account object currently being used by the program.

So the idea became:

```text
DATABASE
   ↑
   │ persistent update
   │
banking_operations
   │
   ↓
ACTIVE ACCOUNT OBJECT
   │
   │ temporary/in-memory state
   ↓
CURRENT PROGRAM SESSION
```

This was one of the moments where I really understood the difference between **persistent state** and **in-memory state**.

---

# 🧮 Working With Money

Another thing I learnt was not to casually depend on floating-point values when storing actual monetary balances.

Instead of storing:

```python
100.50
```

I used pesewas:

```python
10050
```

So:

```text
GHC 1.00 = 100 pesewas
GHC 10.50 = 1050 pesewas
GHC 100.75 = 10075 pesewas
```

This makes calculations easier to keep consistent because the database stores whole integer values.

Then when displaying the balance:

```python
balance / 100
```

converts it back to GHC.

This also made me understand that **display format and storage format don't always have to be the same thing**.

---

# 🧩 Functions, Parameters and Arguments

During this project I became much more comfortable with functions.

I learnt that a parameter is the variable defined by the function:

```python
def deposit(account):
```

while the argument is the actual value passed when calling it:

```python
deposit(active_account)
```

I also learnt how multiple parameters work and how keyword arguments can make calls clearer.

For example:

```python
Account(
    account_number=account_number,
    account_label=account_label,
    account_type=account_type
)
```

This became useful throughout the project because I was creating different objects with many attributes.

---

# 🔁 `return` vs `print`

Another thing I had to properly understand was the difference between:

```python
print()
```

and:

```python
return
```

`print()` displays something to the user.

`return` sends a value back to wherever the function was called.

For example:

```python
def get_balance():
    return balance
```

Then:

```python
current_balance = get_balance()
```

stores the returned value.

I also learnt why I sometimes saw:

```text
None
```

when calling a function inside `print()`.

If a function doesn't explicitly return a value, Python returns:

```python
None
```

So:

```python
print(my_function())
```

can display `None` if `my_function()` only performs an action and doesn't return anything.

This helped me understand why sometimes I wanted a function to **perform an action**, while other times I wanted it to **give a value back**.

---

# 🔐 PIN Verification and Indexing

The Account PIN system taught me another important lesson about handling user input.

I used a 4-digit PIN and stored the PIN as a hash rather than storing the actual PIN.

During verification:

```text
User enters PIN
       ↓
Authentication module
       ↓
Compare against stored hash
       ↓
True / False
```

I also encountered an indexing problem while handling PIN verification and fixed it.

This reminded me that Python indexes things starting from:

```text
0
```

while users normally see choices starting from:

```text
1
```

So when displaying:

```text
[1] Account A
[2] Account B
[3] Account C
```

the corresponding Python indexes are:

```text
0 → Account A
1 → Account B
2 → Account C
```

That was especially important when I allowed a customer to select an account from multiple accounts.

---

# 👤 Session Management

The project also made me understand why I needed a session object.

Instead of passing the customer and account information everywhere manually, the session keeps track of the currently authenticated customer and active account.

The basic idea became:

```text
Login
  ↓
Customer authenticated
  ↓
Start session
  ↓
Customer dashboard
  ↓
Select account
  ↓
Bind active account
  ↓
Account operations
```

When the customer logs out:

```python
session.clear_session()
```

clears the active session state.

I also fixed the naming issue where the session method was originally called something different when what I actually intended was to **clear the session**.

That might sound small, but naming things correctly makes the code much easier to understand later.

---

# 🧪 Testing With Pytest

Testing was one of the final stages of the project.

I used `pytest` to test different parts of the system instead of just running the whole program manually and assuming everything worked.

The important thing I learnt here is that passing tests don't mean:

> “There can never be a bug.”

It means:

> “The behaviours that I wrote tests for are currently behaving as expected.”

During testing, when an issue appeared, I traced it back, fixed the actual problem and ran the tests again.

After going through the final testing stage, the tests passed successfully.

That gave me more confidence that the implementation was not only working when I manually used it through the terminal, but that the individual components were also behaving as expected.

---

# 🧠 What I Finally Learnt From The Project

This project started as me trying to understand Python better, especially functions and classes.

But it ended up teaching me much more than just Python syntax.

I had to understand how different parts of a real program communicate with each other.

The final structure became something like:

```text
                CODE LEGION BANK
                       │
                       ▼
                  main.py
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 Authentication     Session       Workflows
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                  Bank Objects
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
         Customers            Accounts
             │                   │
             └─────────┬─────────┘
                       ▼
                    Database
                       │
                       ▼
                 Transactions
```

I also learnt that building a program is not just about making it run.

I had to think about:

* how objects hold information
* how functions communicate
* how data moves between modules
* how authentication works
* how passwords and PINs should be handled
* how database data differs from memory data
* how transactions should behave
* how sessions should be managed
* how invalid user input should be handled
* how to test individual pieces
* how to debug problems instead of just changing random lines until something works

And probably the biggest lesson for me was that **understanding why the code works is more important than just getting the code to work**.

There were several times during this project where I had something working but didn't fully understand why it was working.

Going back to those parts and breaking them down helped me understand Python much better.

So this project wasn't just:

```text
Build a bank program
```

For me it was more like:

```text
Python
   ↓
Functions
   ↓
Classes & Objects
   ↓
Modules
   ↓
Authentication
   ↓
Database
   ↓
Sessions
   ↓
Transactions
   ↓
Testing
   ↓
A complete working program
```

And that's probably the main reason I learnt so much from building it.
