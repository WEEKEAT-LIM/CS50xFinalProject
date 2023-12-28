"""
This is a module that provides functions to access the database and perform various operations on it. 
\nThe main functions include Get, Check, Create, Add and Update.
\nThis module does not provide any delete functions because of security purpose. . 
\nUser must from DBFunctions import * before using this module.
\nAll function names in this module start with D, followed by the name of the function (initial capitals) and finally the element to be accessed (initial capitals).
"""
from sqlite3 import *
from Components import *

GENERAL = connect("./Database/general.db", check_same_thread=False)
HISTORY = connect("./Database/history.db", check_same_thread=False)
Gcursor = GENERAL.cursor()
Hcursor = HISTORY.cursor()

def DGetUsers():
    """get table called users in general database, return a list"""
    rows = Gcursor.execute("SELECT * FROM users")
    logs = []
    for row in rows:
        tempDict = {"id":row[0], "username":row[1], "password":row[2], "income":row[3]}
        logs.append(tempDict)
    return logs

def DCheckUser(username:str):
    "check username by searching username in table called users in general database, return boolean type"
    dataSet = DGetUsers()
    for data in dataSet:
        if data["username"] == username:
            return True
    print(f"{username} Does Not Exists")
    return False

def DGetUserByUsername(username:str):
    "get user by matching username in table called users in general database, return dictionary or None"
    dataSet = DGetUsers()
    for data in dataSet:
        if data["username"] == username:
            return data
    return None

def DGetProperties():
    """get table called properties in general database, return a list"""
    rows = Gcursor.execute("SELECT * FROM properties")
    logs = []
    for row in rows:
        tempDict = {"id":row[0], "owner":row[1], "propertyName":row[2], "address":row[3], "unitProvided":row[4], "pricePerMonth":row[5], "availableUnits":row[6]}
        logs.append(tempDict)
    return logs

def DGetPropertyByOwner(username:str):
    """get rows by matching username, return a list"""
    logs = []
    rows = DGetProperties()
    for row in rows:
        if row["owner"] == username:
            logs.append(row)
    return logs

def DGetPropertyByPropertyName(propertyName:str):
    """get row by matching property name, return a dictionary or None"""
    rows = DGetProperties()
    for row in rows:
        if row["propertyName"] == propertyName:
            return row
    return None

def DGetHistory(username:str):
    """get table called <username> in history database, return a list or None"""
    if type(username) == str:
        rows = Hcursor.execute("SELECT * FROM %s ORDER BY time DESC"%username)
        logs = []
        for row in rows:
            tempDict = {"id":row[0], "payerName":row[1], "months":row[2], "time":row[3], "propertyName":row[4], "rentedUnit":row[5], "type":row[6]}
            logs.append(tempDict)
        return logs
    else :
        print("TypeError: parameter must be a string => DGetHistory()")
        return None

def DCreateHistory(username:str):
    """create table called <username> in history database,return boolean type"""
    if type(username) == str:
        username = str(username)
        Hcursor.execute("CREATE TABLE %s(id INTEGER PRIMARY KEY AUTOINCREMENT,payerName TEXT NOT NULL,months INTEGER NOT NULL,time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,propertyName TEXT NOT NULL,rentedUnit INTEGER NOT NULL,type TEXT NOT NULL)" %username)
        return True

    else:
        print("TypeError: parameter must be a string => DCreateHistory()")
        flash("📢 Input INVALID!")
        return False

def DAddUser(username, password):
    """add row to table called users in general database, return boolean type"""
    if type(username)==str and type(password)==str:
        Gcursor.execute("INSERT INTO users (username, password, income) VALUES (?, ?, ?)", (username, password, 0))
        GENERAL.commit()
        return True
    else:
        print("TypeError: parameter must be a string => DAddUser()")
        flash("📢 Input INVALID!")
        return False

def DAddProperty(owner, propertyName, address, unitProvided, pricePerMonth, availableUnits):
    """add row to table called properties in general database, return boolean type"""
    if type(owner)!=str and type(propertyName)!=str and type(address)!=str:
        print("TypeError: owner, propertyName, address must be a string =>DAddProperty()")
        flash("📢 Input INVALID!")
        return False
    if type(unitProvided)!=int and type(availableUnits)!=int:
        print("TypeError: unitProvided and availableUnits must be a string =>DAddProperty()")
        flash("📢 Input INVALID!")
        return False
    if type(pricePerMonth)!=float:
        print("TypeError: pricePerMonth must be a float or integer =>DAddProperty()")
        flash("📢 Input INVALID!")
        return False

    Gcursor.execute("INSERT INTO properties (owner, propertyName, address, unitProvided, pricePerMonth, availableUnits) VALUES(?, ?, ?, ?, ?, ?)",
                    (owner, propertyName, address, unitProvided, pricePerMonth, availableUnits))
    GENERAL.commit()
    return True

def DAddHistory(username:str, payerName:str, months:int, propertyName:str, rentedUnit:int, types:str):
    """add row to table called <username> in history database, return boolean type"""
    bUserExists = DCheckUser(username=username)
    if bUserExists == False :
        flash("📢 username INVALID!")
        return False
    if type(payerName)!=str and type(propertyName)!=str and type(type)!=str:
        print("TypeError: payerName, propertyName and type must be a string => DAddhistory()")
        flash("📢 Input INVALID!")
        return False
    if type(months)!=int and type(rentedUnit)!=int:
        print("TypeError: months and rentedUnit must be a string =>DAddHistory()")
        flash("📢 Input INVALID!")
        return False
    if types != "Check In" and types!= "Check Out":
        print("ValueError: type must be 'Check In' or 'Check Out' => DAddHistory()")
        flash("📢 Input INVALID!")
        return False
    
    data = DGetPropertyByPropertyName(propertyName=propertyName)

    if types == "Check In":
        if data["availableUnits"] < rentedUnit:
            print("available units less than rented unit =>DAddHistory")
            flash("📢 UNIT INVALID!")
            return redirect("/")
        availableUnits = data["availableUnits"] - rentedUnit
        data2 = DGetUsers()
        data2_result = []
        for i in data2:
            if i["username"] == username:
                data2_result.append(i)

        totalIncome = (months * data["pricePerMonth"] * rentedUnit) + data2_result[0]["income"]
        Gcursor.execute("UPDATE properties SET availableUnits=? WHERE propertyName=? AND owner=?",(availableUnits, propertyName, username))
        Gcursor.execute("UPDATE users SET income=? WHERE username=?",(totalIncome, username))
        GENERAL.commit()

    if types == "Check Out":
        if data["availableUnits"] + rentedUnit > data["unitProvided"]:
            print("available units + rented unit larger than unit provided =>DAddHistory")
            flash("📢 UNIT INVALID!")
            return redirect("/")
        availableUnits = data["availableUnits"] + rentedUnit
        data2 = DGetUsers()
        data2_result = []
        for i in data2:
            if i["username"] == username:
                data2_result.append(i)
        Gcursor.execute("UPDATE properties SET availableUnits=? WHERE propertyName=? AND owner=?",(availableUnits, propertyName, username))
        GENERAL.commit()

    Hcursor.execute("INSERT INTO %s (payerName, months, propertyName, rentedUnit, type) VALUES(?, ?, ?, ?, ?)"%username,(payerName, months, propertyName, rentedUnit, types))
    HISTORY.commit()
    return True

def DUpdateProperty(owner, propertyName, Naddress, NunitProvided, NpricePerMonth):
    """parameter start with N mean new value, return boolean type"""
    data = DGetPropertyByPropertyName(propertyName)
    availableUnits = data["availableUnits"]
    if data != None and data["unitProvided"] < NunitProvided:
        availableUnits = (NunitProvided - data["unitProvided"]) + availableUnits
        Gcursor.execute("UPDATE properties SET address=?, unitProvided=?, pricePerMonth=?, availableUnits=? WHERE propertyName=? AND owner=?", 
                        (Naddress, NunitProvided, NpricePerMonth, availableUnits, propertyName, owner))
        GENERAL.commit()
        return True
    if data != None and data["unitProvided"] > NunitProvided:
        availableUnits = availableUnits - (data["unitProvided"] - NunitProvided)
        Gcursor.execute("UPDATE properties SET address=?, unitProvided=?, pricePerMonth=?, availableUnits=? WHERE propertyName=? AND owner=?", 
                        (Naddress, NunitProvided, NpricePerMonth, availableUnits, propertyName, owner))
        GENERAL.commit()
        return True
    if data != None and data["unitProvided"] == NunitProvided:
        Gcursor.execute("UPDATE properties SET address=?, unitProvided=?, pricePerMonth=?, availableUnits=? WHERE propertyName=? AND owner=?", 
                        (Naddress, NunitProvided, NpricePerMonth, availableUnits, propertyName, owner))
        GENERAL.commit()
        return True
    flash("📢 Update failed, please try again!")
    print("Update failed => DUpdateProperty")
    return False



if __name__ == "__main__":
    print("Running DBFunctions...")
    # test
    print("END RUN :)")