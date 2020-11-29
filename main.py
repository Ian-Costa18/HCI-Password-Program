from flask import Flask, request
from random import randint
import bcrypt
import json

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

    for db_user in db["users"]:
        if username.lower() == db_user["username"].lower():
            # Loop over each possible pepper
            for p in range(1, pepper_range):
                # Check the password for the current pepper
                pepp_passwd = passwd + str(p)
                found = bcrypt.checkpw(pepp_passwd.encode("utf-8"), db_user["password"].encode("utf-8"))
                # return the result if found
                if found:
                    return db_user
            # If the loop finishes without finding the password, return false
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

    checked = check_user(username, password)
    if checked:
        return 'You are successfully logged in! <a href="/login">Return to login</a>, <a href="/create-account">Create another account</a>, or <a href="/change-password">Change your password</a>'

    return "Failed, your username or password was not found in our database"


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return app.send_static_file("create-account.html")

    values = request.values
    username, password = values["username"], values["password"]
    salt = bcrypt.gensalt()
    with open("us2rdb.json", "r") as file:
        db = json.load(file)

    user = {
        "username": username,
        "password": hash(password, salt).decode("utf-8"),
        "saltnpepper": [salt.decode("utf-8"), PEPP]
    }

    for db_user in db["users"]:
        if user["username"].lower() == db_user["username"].lower():
            return "User already in database, please either change your username or update your password here"

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

    if not user:
        return "Username or password is not found in our database."

    # Create new password hash
    salt = bcrypt.gensalt()


    user["password"] = hash(new_password, salt).decode("utf-8")
    user["saltnpepper"] = [salt.decode("utf-8"), PEPP]

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
