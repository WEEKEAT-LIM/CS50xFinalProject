from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from Components import *
from DBFunctions import *

app = Flask("__name__")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    username = DGetUsers()[session["user_id"] - 1]["username"]
    IdataSet = DGetPropertyByOwner(username)
    TotalIncome = DGetUserByUsername(username)["income"]
    TotalIncome = currency("MYR",TotalIncome)
    return render_template("index.html", IDataSet=IdataSet, totalIncome=TotalIncome)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    flash("📢 Log out successful!")
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        Rusername = request.form.get("username")
        Rpassword = request.form.get("password")
        Rconfirmation = request.form.get("confirm")
        
        # Authentic
        if not Rusername:
            flash("📢 Missing username")
            return redirect("/register")
        elif not Rpassword:
            flash("📢 Missing passowrd")
            return redirect("/register")
        elif not Rconfirmation:
            flash("📢 Missing confirmation")
            return redirect("/register")
        if Rconfirmation != Rpassword:
            flash("📢 INVALID Confirmation")
            return redirect("/register")
        row = DGetUserByUsername(Rusername)
        if row != None:
            flash("📢 Username already exists, please try again")
            return redirect("/register")

        session.clear()
        Rpassword =  generate_password_hash(Rpassword)
        DAddUser(Rusername, Rpassword)
        DCreateHistory(Rusername)
        session["user_id"] = DGetUserByUsername(Rusername)["id"]
        flash("📢 Register successful!")
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session.clear()
        Lusername = request.form.get("username")
        Lpassword = request.form.get("password")
        bInput = check_input(Lusername,Lpassword,redirect_path="/login")
        if bInput != True:
            return redirect(bInput)

        rows = DGetUsers()
        for row in rows:
            if (row["username"] == Lusername) and (check_password_hash(row["password"],Lpassword)):
                session["user_id"] = row["id"];
                flash("📢 Log in successful!")
                return redirect("/")
        
        flash("📢 Username or password INVALID => Please try again!")
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/add_property", methods=["GET","POST"])
@login_required
def add_property():
    if request.method == "POST":
        Aowner = DGetUsers()[session["user_id"] - 1]["username"]
        ApropertyName = request.form.get("propertyName")
        Aaddress = request.form.get("address")
        AunitProvided = request.form.get("unitProvided")
        ApricePerMonth = request.form.get("pricePerMonth")
        AavailableUnits = AunitProvided

        bInput = check_input(ApropertyName, Aaddress, AunitProvided, ApricePerMonth, redirect_path="/")
        if bInput != True:
            return redirect(bInput)

        if DGetPropertyByPropertyName(ApropertyName) != None:
            flash("📢 Property name already exists!")
            return redirect("/")
        
        if StringToInt(AunitProvided) == None or StringToFloat(ApricePerMonth)==None:
            flash("📢 Unit provided & price must be integer or float only")
            return redirect("/")

        DAddProperty(Aowner, ApropertyName, Aaddress, StringToInt(AunitProvided), StringToFloat(ApricePerMonth),AavailableUnits)
        flash("📢 Property added!")
        return redirect("/")
    else:
        return render_template("add_property.html")

@app.route("/update_property", methods=["GET", "POST"])
@login_required
def update_property():
    Uowner = DGetUsers()[session["user_id"] - 1]["username"]
    properties = DGetPropertyByOwner(Uowner)
    if request.method == "POST":
        UpropertyName = request.form.get("propertyName")
        Uaddress = request.form.get("address")
        UunitProvided = request.form.get("unitProvided")
        UpricePerMonth = request.form.get("pricePerMonth")

        bInput = check_input(UpropertyName, Uaddress, UunitProvided, UpricePerMonth,redirect_path="/")
        if bInput != True:
            return redirect(bInput)
        
        if DGetPropertyByPropertyName(UpropertyName) == None:
            flash(f"📢 {UpropertyName} does not exists!")
            return redirect("/")

        UunitProvided = StringToInt(UunitProvided)
        UpricePerMonth = StringToFloat(UpricePerMonth)
        if UunitProvided == None or UpricePerMonth==None:
            flash("📢 Unit provided & price must be integer or float only")
            return redirect("/")
        
        bUpdate = DUpdateProperty(Uowner,UpropertyName, Uaddress, UunitProvided, UpricePerMonth)
        if bUpdate == True:
            flash("📢 Property updated!")
            return redirect("/")
        
        return redirect("/")
    else:
        return render_template("update_property.html", dataSet=properties)

@app.route("/CheckIn", methods=["GET","POST"])
@login_required
def CheckIn():
    Cowner = DGetUsers()[session["user_id"] - 1]["username"]
    properties = DGetPropertyByOwner(Cowner)
    if request.method =="POST":
        CpropertyName = request.form.get("propertyName")
        CpayerName = request.form.get("payerName")
        Cmonths = request.form.get("months")
        CrentedUnit = request.form.get("rentedUnit")

        bInput = check_input(CpropertyName, CpayerName, Cmonths, CrentedUnit,redirect_path="/")
        if bInput != True:
            return redirect(bInput)
        
        if DGetPropertyByPropertyName(CpropertyName) is None:
            flash(f"📢 {CpropertyName} does not exists!")
            return redirect("/")
        
        Cmonths = StringToInt(Cmonths)
        CrentedUnit = StringToInt(CrentedUnit)
        if CrentedUnit == None or Cmonths==None:
            flash("📢 Units & months must be integer only")
            return redirect("/")
        
        bAdd = DAddHistory(Cowner, CpayerName, Cmonths, CpropertyName, CrentedUnit, "Check In")
        if bAdd == True:
            flash("📢 Check in successful!")
            return redirect("/")
        
        return redirect("/")
    else:
        return render_template("check_in.html", dataSet=properties)
    
@app.route("/CheckOut", methods=["GET", "POST"])
@login_required
def CheckOut():
    C2owner = DGetUsers()[session["user_id"] - 1]["username"]
    C2properties = DGetPropertyByOwner(C2owner)
    if request.method =="POST":
        C2propertyName = request.form.get("propertyName")
        C2payerName = request.form.get("payerName")
        C2months = request.form.get("months")
        C2rentedUnit = request.form.get("rentedUnit")

        bInput = check_input(C2propertyName, C2payerName, C2months, C2rentedUnit,redirect_path="/")
        if bInput != True:
            return redirect(bInput)
        
        if DGetPropertyByPropertyName(C2propertyName) ==None:
            flash(f"📢 {C2propertyName} does not exists!")
            return redirect("/")
        
        C2months = StringToInt(C2months)
        C2rentedUnit = StringToInt(C2rentedUnit)
        if C2rentedUnit == None or C2months==None:
            flash("📢 Units & months must be integer only")
            return redirect("/")
        
        bAdd = DAddHistory(C2owner, C2payerName, C2months, C2propertyName, C2rentedUnit, "Check Out")

        if bAdd == True:
            flash("📢 Check out successful!")
            return redirect("/")
        
        return redirect("/")
    else:
        return render_template("check_out.html", dataSet=C2properties)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    username = DGetUsers()[session["user_id"] - 1]["username"]
    dataSet = DGetHistory(username=username)
    return render_template("history.html", DataSet=dataSet)

@app.route("/LICENSE", methods=["GET","POST"])
def license():
    return render_template("LICENSE.html")

if __name__ == "__main__":
    print("Running app.py...")
    app.run()
    print("END RUN :)")