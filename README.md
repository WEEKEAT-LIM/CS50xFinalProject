# Rental Recorder

Rental Recorder is a web app implemented using Flask, Bootstrap and SQLite that works as a mini recorder to help house owners track their properties.
<br>

> Video Demo: https://youtu.be/Fs_bsjnPy-A

> ![project structure](src/Final%20Project%20-%20STRUCTURE.jpg)
> project structure
> <br> > `users` (table) and `properties` (table) storing in `general.db` > <br> > `<username>`(table) storing in `history.db`

<br>

> ![project workflow](src/Final%20Project%20-%20Workflow.jpg)
> project workflow

### Features

- **Register** : Everyone can register to make a new account.
- **Dashboard** : The user can see the total income and details of properties in card view when they log in.
- **History** : The user can see the past transaction history.
- **Add property** : The user can add the property.
- **Update property** : The user can update the details of the property.
- **Check in** : The user can add the transaction when someone checks in.
- **Check out** : The user can add the transaction when someone checks out.

> All properties names must be different (even if owned by different user) and property names are unique

<br>

---

## Modules

### DBFunctions.py

DBFunctions provides functions to access the database and perform various operations on it. The main functions include `Get`, `Check`, `Create`, `Add` and `Update`.Some of them also can use with `By` query.
This module does not provide any delete functions because of security purpose.User must `from DBFunctions import \*` before using this module.All function names in this module start with D, followed by the name of the function (initial capitals) and finally the element to be accessed (initial capitals).Example => `DGetUserByUsername(username:str)`<br>
[DBFunctions Documentation](./Documentation/DBFunctions.md)

### Components.py

Components provides some functions are auxiliary in this project.User must `from components import \*` before using this module. `login_required` function is used to make sure the user is logged in before performing any operation. `check_input<R>` function is used to make sure the user does not pass empty parameters or else it returns redirect or render_template path. `currency` function is used to make sure the front-end outputs with custom currency symbol like USD, MYR, etc. ensure front-end outputs currency with custom symbols such as USD, MYR, etc. Functions starting with `StringTo<type>` are used to convert the user-entered string to an integer or floating-point number.
<br>
[Components Documentation](./Documentation/Components.md)

<br>

---

## Details of database structure

### users [table]

Storing `username` , `password` and `current income`.
Create a row when someone \<register>.

### properties [table]

Storing `property owner` , `property name` , `address` , `unit provided` and `price per month for 1 unit`. Create a row when user \<add property>. Update data when user \<update property>.

### history [database]

Storing `payer name` , `months` , `timestamp` , `property name` , `rented unit`.Create a table named \<username> when someone \<register> . Create a row when user \<check in> or \<check out> .

<br>

---

## Details of templates

- `layout.html` : template
- `index.html` : provide a dashboard can showing the details of properties by card view.
- `login.html` : provide a form for user to login their account
- `register.html` : provide a form for someone who want to create a new account
- `add_property.html` : provide a form for user to add their property
- `update_property.html` : provide a form for user to update the information of the property
- `check_in.html` and `check_out.html` : provide a form for user to record details of "rental"
- `history.html` : showing all records by table view

<br>

---

## Run on your local machine

### requirements

check by using command `pip install -r .\requirements.txt`

```
- python3
- Flask 3.0.0++
- Flask-Session 0.5.0++
- Werkzeug 3.0.1++
- Jinja2 3.1.2++
- itsdangerous 2.1.2++
- ...
```

1. create a new directory
2. download `.zip`
3. export to the directory
4. run terminal in directory
5. execute command `flask run` ; return=> ` * Running on http://127.0.0.1:5000`
6. click the link to localhost => `http://127.0.0.1:5000`

<br>

---

## Reference:

1. <a href="https://www.flaticon.com/free-icons/rent" title="rent icons">Rent icons created by Freepik - Flaticon</a>
2. <a href="https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.after_request_funcs" title="Flask">Flask Documentation</a>
3. <a href="https://werkzeug.palletsprojects.com/en/3.0.x/" title="werkzeug">werkzeug Documentation</a>
4. <a href="https://getbootstrap.com/docs/5.3/getting-started/introduction/" title="Bootstrap">Bootstrap</a>
5. <a href="https://docs.python.org/3/library/sqlite3.html" title="Python SQLite3">Python SQLite3</a>

<br>

---

## Tech Stack

- Python (Flask, werkzeug)
- HTML
- CSS
- Java Script
- SQLite3
