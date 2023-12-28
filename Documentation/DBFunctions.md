# DBFunctions

This is a module that provides functions to access the database and perform various operations on it.
<br>The main functions include `Get`, `Check`, `Create`, `Add` and `Update`.
<br>This module does not provide any delete functions because of security purpose. .
<br>User must from DBFunctions import \* before using this module.
<br>All function names in this module start with D, followed by the name of the function (initial capitals) and finally the element to be accessed (initial capitals).

```python
from sqlite3 import *
from components import *

GENERAL = connect("./Database/general.db", check_same_thread=False)
HISTORY = connect("./Database/history.db", check_same_thread=False)
Gcursor = GENERAL.cursor()
Hcursor = HISTORY.cursor()
```

> 🛠️ Note: All functions that return unintended results will print a prompt in the terminal for optimization or debugging.

<br>

---

## DGet...

### DGetUsers()

select all from table called users in general database
<br>
`return` : `list`
<br>

### DGetProperties()

select all from table called users in general database
<br>
`return` : `list`
<br>

### DGetHistory(username:str)

select all form table called \<username> in history database
<br>
`username` : username
<br>
`return` : `list` OR `None`

<br>

### DGetUserByUsername(username:str)

get user by matching username in table called users in general database
<br>
`username` : username
<br>
`return` : `dictionary` OR `None`
<br>

### DGetPropertyByOwner(username:str)

get rows by matching username from table called properties in general database
<br>
`username` : property owner
<br>
`return` : `list` OR `None`
<br>

### DGetPropertyByPropertyName(propertyName:str)

get rows by matching property name from table called properties in general database
<br>
`propertyName` : property name
<br>
`return` : `dictionary` OR `None`

<br>

---

## DCheckUser(username:str)

check username by searching username in table called users in general database
<br>
`username` : username
<br>
`return` : `True` OR `False`

> Action when user does not exists >> `print(f"{username} Does Not Exists")`

<br>

---

## DCreateHistory(username:str)

create table called \<username> in history database
<br>
`username` : username
<br>
`return` : `True` OR `False`

> Action when type of parameter not string >> `flash("📢 Input INVALID!")`

<br>

---

## DAdd...

### DAddUser(username, password)

add row to table called users in general database
<br>
`username` : username
<br>
`password` : account password
<br>
`return` : `True` OR `False`

> Action when type of parameters not string >> `flash("📢 Input INVALID!")`

<br>

### DAddProperty(owner, propertyName, address, unitProvided, pricePerMonth, availableUnits)

add row to table called properties in general database
<br>
`owner` : property owner name
<br>
`propertyName` : property name
<br>
`address` : address of property
<br>
`unitProvided` : total unit of property
<br>
`pricePerMonth` : price per month for 1 unit
<br>
`availableUnits` : initialize by unity provided
<br>
`return` : `True` OR `False`

> Action when parameters type error >> `flash("📢 Input INVALID!")`

<br>

### DAddHistory(username:str, payerName:str, months:int, propertyName:str, rentedUnit:int, types:str)

add row to table called \<username> in history database
<br>
`username` : property owner name
<br>
`payerName` : person who pay for the rent
<br>
`months` : number of month (pay for)
<br>
`propertyName` : property name
<br>
`rentedUnit` : number of unit (pay for)
<br>
`types` : Check In OR Check Out
<br>
`return` : `True` OR `False`

> Action when user does not exists >> `flash("📢 username INVALID!")` ><br>
> Action when parameters type error >> `flash("📢 Input INVALID!")` ><br>
> Action when input units are illogical >> `flash("📢 UNIT INVALID!")`

<br>

---

## DUpdateProperty(owner, propertyName, Naddress, NunitProvided, NpricePerMonth)

update row in table called properties from general database
<br>
`owner` : property owner name
<br>
`propertyName` : property name
<br>
`Naddress` : New address
<br>
`NunitProvided` : new unit provided
<br>
`NpricePerMonth` : new price per month for 1 unit
<br>
`return` : `True` OR `False`

> Action when update failed >> `flash("📢 Update failed, please try again!")`

<br>

---

## Testing DBFunctions

```python
if __name__ == "__main__":
    print("Running DBFunctions...")
    # test
    print("END RUN :)")
```

<br>

### [back to README](../README.md)
