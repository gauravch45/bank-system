from flask import Flask, render_template, request, redirect, url_for
from bank import Bank
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://admin:a6vwMyhKjq1ZUULP@bank-clustor.eefie.mongodb.net/?retryWrites=true&w=majority&appName=bank-clustor"
db_name = "customers"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


bank = Bank(uri, db_name)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    account_number = request.form["account_number"]
    name = request.form["name"]
    balance = float(request.form["balance"])
    bank.create_account(account_number, name, balance)
    return redirect(url_for("index"))

@app.route("/deposit", methods=["POST"])
def deposit():
    account_number = request.form["account_number"]
    amount = float(request.form["amount"])
    bank.deposit(account_number, amount)
    return redirect(url_for("index"))

@app.route("/withdraw", methods=["POST"])
def withdraw():
    account_number = request.form["account_number"]
    amount = float(request.form["amount"])
    bank.withdraw(account_number, amount)
    return redirect(url_for("index"))

@app.route("/check_balance", methods=["POST"])
def check_balance():
    account_number = request.form["account_number"]
    account = bank.get_account(account_number)
    if account:
        balance = account["balance"]
        return render_template("balance.html", balance=balance , account_number = account_number)
    else:
        return "Account not found"

if __name__ == "__main__":
    app.run(debug=True)