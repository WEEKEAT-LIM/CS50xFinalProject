from flask import redirect, render_template, session, redirect, flash
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def check_input(*args,redirect_path:str):
    """return redirect path when missing input"""
    missing = []
    for arg in args:
        if not arg:
            missing.append(arg)

    if len(missing) > 0:
        flash(f"📢 Missing {len(missing)} input")
        return redirect_path
    return True

def check_inputR(*args,render_path:str):
    """Call render_template() when missing input, can't passing any parameter"""
    missing = []
    for arg in args:
        if not arg:
            missing.append(arg)

    if len(missing) > 0:
        flash(f"📢 Missing {len(missing)} input")
        return render_template(render_path)
    return True

def currency(symbol:str, value:float):
    """return currency. Example: symbol="MYR" value=1 return 1.00 MYR"""
    return f"{value:,.2f} {symbol}"

def StringToInt(value:str):
    for i in value:
        if i not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            return None
    return int(value)

def StringToFloat(value:str):
    for i in value:
        if i not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]:
            return None
    return float(value)

if __name__ == "__main__":
    print("Running Components...")
    # test
    print("END RUN :)")