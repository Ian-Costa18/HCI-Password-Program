from flask import Flask, request
from random import randint
import bcrypt
import json
import datetime

app = Flask(__name__)
PEPP = 4 # Number of possible peppers
USERS = []

def hash(passwd, salt, pepper_range=PEPP):

    # Generate pepper
    # Peppers increase hash security by multiples of the pepper
    # Pepper is a small random number appended to password
    # To brute force a password w/ pepper attacker must guess what the pepper is
    # To dehash a password w/ pepper we just need to try each possible pepper until the password's match
    pepper = str(randint(1, pepper_range))
    passwd = passwd + pepper

    hashed = bcrypt.hashpw(passwd.encode('utf_8'), salt)

    return hashed

def check_user(username, passwd, pepper_range=PEPP):
    with open("userdb.json", "r") as file:
        db = json.load(file)

    for index, db_user in enumerate(db["users"]):
        if username.lower() == db_user["username"].lower():
            # Loop over each possible pepper
            for p in range(1, pepper_range):
                # Check the password for the current pepper
                pepp_passwd = passwd + str(p)
                found = bcrypt.checkpw(pepp_passwd.encode("utf-8"), db_user["password"].encode("utf-8"))
                # return the result if found
                if found:
                    return db_user
            # If loop finishes without finding password
            numattempts = db["users"][index]["numattempts"]
            numattempts[0] += 1
            if numattempts[1] == str(datetime.date.today()):
                if numattempts[0] >= 10:
                    db["users"][index]["locked"] = True
                    with open("userdb.json", "w") as file:
                        json.dump(db, file)
                    return "Account locked"
            else:
                db["users"][index]["numattempts"][1] = str(datetime.date.today())
            with open("userdb.json", "w") as file:
                json.dump(db, file)
    # If the loop finishes without finding the user, return false
    return False

@app.route("/", methods=["GET"])
def main_page():
    return app.send_static_file("create-account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return app.send_static_file("login.html")

    values = request.values
    username, password = values["username"], values["password"]

    user = check_user(username, password)
    if user == "Account locked":
        return "Too many incorrect attempts, your account has been locked. Please contact the administrator"
    if not user:
        return "Failed, your username or password was not found in our database"
    if (datetime.datetime.strptime(user["lastchanged"], "%Y-%m-%d").date() - datetime.date.today()).days <= -180:
        return 'Your password is over 180 days old and has expired, please <a href="/change-password">change your password here</a> to log in.'

    return f'You are successfully logged in! <a href="/login">Return to login</a>, <a href="/create-account">Create another account</a>, or <a href="/change-password">Change your password</a>'


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return app.send_static_file("create-account.html")

    values = request.values
    username, password = values["username"], values["password"]
    salt = bcrypt.gensalt()
    hashed_password = hash(password, salt).decode("utf-8")
    with open("userdb.json", "r") as file:
        db = json.load(file)

    user = {
        "username": username.lower(),
        "password": hashed_password,
        "saltnpepper": [salt.decode("utf-8"), PEPP],
        "numattempts": [0, str(datetime.date.today())],
        "locked": False,
        "lastchanged": str(datetime.date.today()),
        "previouspasswords": []
    }

    for db_user in db["users"]:
        if user["username"].lower() == db_user["username"].lower():
            return "User already in database, please either change your username or <a href='/change-password'>update your password here</a>"

    db["users"].append(user)

    with open("userdb.json", "w") as file:
        json.dump(db, file)

    return 'Success! <a href="/login">Log In Here!</a>'


@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return app.send_static_file("change-password.html")

    values = request.values
    username, old_password, new_password = values["username"], values["old-password"], values["new-password"]

    user = check_user(username, old_password)

    if user == "Account locked":
        return "Too many incorrect attempts, your account has been locked. Please contact the administrator"

    if not user:
        return "Username or password is not found in our database."
    days_since_change = (datetime.datetime.strptime(user["lastchanged"], "%Y-%m-%d").date() - datetime.date.today()).days
    if days_since_change == 0:
        return "You cannot change your password more than once a day."

    # Create new password hash
    salt = bcrypt.gensalt()

    # Add the old password to previous password list before overwriting
    user["previouspasswords"] = (user["previouspasswords"] + [user["password"]])[-10:]
    user["password"] = hash(new_password, salt).decode("utf-8")
    user["saltnpepper"] = [salt.decode("utf-8"), PEPP]
    user["lastchanged"] = str(datetime.date.today())

    for pepper in range(PEPP):
        test_password = new_password + str(pepper+1)
        hashed_test_pass = bcrypt.hashpw(test_password.encode("utf-8"), salt).decode("utf-8")
        if hashed_test_pass in user["previouspasswords"]:
            return "Failed, your new password cannot be the same as one of your previous 10 passwords."

    with open("userdb.json", "r") as file:
        db = json.load(file)

    for index, db_user in enumerate(db["users"]):
        if user["username"].lower() == db_user["username"].lower():
            db["users"][index] = user

    with open("userdb.json", "w") as file:
        json.dump(db, file)

    return 'Success! <a href="/login">Log In Here!</a>'


if __name__ == '__main__':
    app.run()
