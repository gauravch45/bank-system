from pymongo import MongoClient

class Bank:
    def __init__(self, mongo_uri, db_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def create_account(self, account_number, name, balance):
        self.db.accounts.insert_one({"account_number": account_number, "name": name, "balance": balance})

    def get_account(self, account_number):
        return self.db.accounts.find_one({"account_number": account_number})

    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            balance = account["balance"] + amount
            self.db.accounts.update_one({"account_number": account_number}, {"$set": {"balance": balance}})

    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            balance = account["balance"] - amount
            if balance >= 0:
                self.db.accounts.update_one({"account_number": account_number}, {"$set": {"balance": balance}})
            else:
                print("Insufficient balance")

    def close_connection(self):
        self.client.close()