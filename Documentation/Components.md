# Components Documentation

```python
from flask import redirect, render_template, session, redirect, flash
from functools import wraps
```

<br>

---

## login_required(f)

Decorate routes to require login.
http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/

<br>

---

## check_input(\*args,redirect_path:str)

looping the args to check the number of missing input
<br>
`*args` : user input
<br>
`redirect_path`: redirect path when user missing input
<br>
`return` : `True` OR `redirect(redirect_path)`
<br>

> Action when missing input >> `flash(f"📢 Missing {len(missing)} input")`

<br>

---

## check_inputR(\*args,render_path:str)

looping the args to check the number of missing input
<br>
`*args` : user input
<br>
`render_path` : render path when user missing input
<br>
`return` : `True` OR `render_template(render_path)`
<br>

> Action when missing input >> `flash(f"📢 Missing {len(missing)} input")`

<br>

---

## currency(symbol:str, value:float)

formatting value. Example: symbol="MYR" value=1 return 1.00 MYR
<br>
`symbol` : custom currency symbol
<br>
`value` : integer or float
<br>
`return` : \<formatted value> \<symbol>

<br>

---

## StringToInt(value:str)

convert the user-entered string to an integer
<br>
`value` : string only include 0 to 1, without `-` or `+`
<br>
`return` : integer
<br>

> Action when value invalid >> `return None`

<br>

---

## StringToFloat(value:str)

convert the user-entered string to an float
<br>
`value` : string only include 0 to 1 and `.` , without `-` or `+`
<br>
`return` : float
<br>

> Action when value invalid >> `return None`

<br>

---

## Testing Components

```python
if __name__ == "__main__":
    print("Running Components...")
    # test
    print("END RUN :)")
```

<br>

### [back to README](../README.md)
