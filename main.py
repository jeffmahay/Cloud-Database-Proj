import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Setup Google Cloud Key - The json file is obtained by going to 
# Project Settings, Service Accounts, Create Service Account, and then
# Generate New Private Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "helloworld-ff866-firebase-adminsdk-8g5cm-fb6a35ccca.json"

# Use the application default credentials.  The projectID is obtianed 
# by going to Project Settings and then General.
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'helloworld-ff866',
})

db = firestore.client()

def user_list():
    '''
    Prints out each document id in the bankapp collection
    '''
    translate_list = []
    print("Users: ")
    for i in get_user():
        if i.exists:
            print(f"{i.id}")
            translate_list.append(i.id)
        else:
            print("User does not exist\n")
    return translate_list

def get_user():
    '''
    Gets a list of documents in the bankapp collection
    '''
    documents = db.collection("bankapp").get()
    return documents

def view_ind(user):
    '''
    Returns the balance of a specific user
    USER = name of the document to access
    '''
    bank = db.collection("bankapp").document(user).get()
    if bank.exists:
        info = bank.to_dict()
        return float(info["balance"])
    else:
        print(f"Error, {user} does not equal {bank.id}")

def view_comb():
    '''
    Accesses each of the document's field info and stores them into a list
    '''
    total = 0.0
    for document in db.collection("bankapp").get():
        info = document.to_dict()
        total += float(info["balance"])
    return total

def add_person():
    '''
    Creates a new document in the bankapp collection with the balance field
    '''
    user = input("Person's Name: ")
    balance = float(input("Balance: "))

    result = db.collection("bankapp").document(user).get()
    if result.exists:
        print("User already exists.")
        return

    data = {
        "balance" : balance
        }
    
    db.collection("bankapp").document(user).set(data) 
    print("New person added to database!\n")
    log_data(f"{user} added to database")

def remove_person(user):
    '''
    Removes a document in the bankapp collection
    USER = specifies which document to access
    '''
    result = db.collection("bankapp").document(user).get()
    if not result.exists:
        print("User does not exist.")
        return
    else:
        db.collection("bankapp").document(user).delete()
        print(f"{user} has been removed from the database")
        log_data(f"{user} added to database")

def withdraw(user, w_amount):
    '''
    Accesses a user's balance field and subtracts the amount by w_amount
    USER = specifies which document to access
    W_AMOUNT = amount to subtract the balance by
    '''
    result = db.collection("bankapp").document(user).get()
    if not result.exists:
        print("Invalid Item Name")
        return

    data = result.to_dict()

    data["balance"] -= w_amount
    db.collection("bankapp").document(user).set(data)
    log_data(f"{w_amount} has been withdrawn from {user}'s balance.")

def deposit(user, d_amount):
    '''
    Accesses a user's balance field and adds the amount by d_amount
    USER = specifies which document to access
    D_AMOUNT = amount to increase the balance by
    '''
    result = db.collection("bankapp").document(user).get()
    if not result.exists:
        print("Invalid Item Name")
        return

    data = result.to_dict()

    data["balance"] += d_amount
    db.collection("bankapp").document(user).set(data)
    log_data(f"{d_amount} has been added to {user}'s balance.")

def log_data(message):
    '''
    Adds a randomly generated document to the log collection which has fields which say what was changed
    and what time it was changed at
    MESSAGE = message to be written in the field
    '''
    data = {"message" : message, "timestamp" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)    

def split_even(bill):
    '''
    Divides the provided bill by 2
    BILL = cost of bill
    '''
    print("Amount owed by both people: ")
    print(f"${float(bill/2)}")

def split_percent(bill, user1, user2):
    '''
    Divides the bill by a percentage of the total balance of two users
    BILL = cost of bill
    USER1 = document to access 
    USER2 = document to access
    '''
    user1_field = db.collection("bankapp").document(user1).get()
    user_1_read = user1_field.to_dict()
    user_1_total = float(user_1_read['balance'])

    user2_field = db.collection("bankapp").document(user2).get()
    user_2_read = user2_field.to_dict()
    user_2_total = float(user_2_read['balance'])

    total_money = user_1_total + user_2_total

    user_1_share = (user_1_total / total_money) * bill
    user_2_share = (user_2_total / total_money) * bill

    return round(user_1_share, 2), round(user_2_share, 2)

def notify_low_balance(results, changes, read_time):
    '''
    If the user is low on balance, then display the changes.
    ADDED = New user added to the list since registration
    MODIFIED = A user balance was modified but still too low
    REMOVED = A user balance is no longer too low
    '''
    for change in changes:
        if change.type.name == "ADDED": 
            print()
            print(f"WARNING!! {change.document.id}'s BALANCE IS LOW")
            print()
        elif change.type.name == "REMOVED":
            print()
            print(f"{change.document.id}'s BALANCE IS NO LONGER LOW")
            print()
    
def register_low_balance(warning):
    '''
    Request a query to be monitored.  If the query changes, then the
    notify_low_balance will be called.
    '''
    db.collection("bankapp").where("balance","<=",warning).on_snapshot(notify_low_balance)


def main():
    '''
    Creates the menu, and an if/else chain inside a while loop to navigate the menu
    '''
    choice = -1
    warning = float(50)


    print("Welcome! Please select an option below: ")

    while choice != 0:
        print("0.Exit application")
        print("1.View individual balance")
        print("2.View combined balance")
        print("3.Add a person")
        print("4.Remove a person")
        print("5.Make a withdraw")
        print("6.Make a deposit")
        print("7.Split a bill")
        print("8.Set balance warning")

        register_low_balance(warning)

        choice = int(input("> "))
        print(" ")

        if choice == 0:
            print("Goodbye!")

        elif choice == 1:
            extract_list = user_list()
            user = input("> ")
            if user in extract_list:
                print(f"User balance: ${view_ind(user)}\n")
            else:
                print("User does not exist \n")

        elif choice == 2:
            print(f"Combined balance: ${view_comb()}\n")

        elif choice == 3:
            add_person()

        elif choice == 4:
            extract_list = user_list()
            user = input("> ")
            if user in extract_list:
                remove_person(user)
                print(f"{user} has been removed from database\n")
            else:
                print("User does not exist \n")

        elif choice == 5:
            extract_list = user_list()
            user = input("> ")
            if user in extract_list:
                print("Please enter an amount to be withdrawn: ")
                w_amount = float(input("> "))
                withdraw(user, w_amount)
                print(f"New balance: ${view_ind(user)}\n")
            else:
                print("User does not exist \n")

        elif choice == 6:
            extract_list = user_list()
            user = input("> ")
            if user in extract_list:
                print("Please enter an amount to be deposited: ")
                d_amount = float(input("> "))
                deposit(user, d_amount)
                print(f"New balance: ${view_ind(user)}\n")
            else:
                print("User does not exist \n")

        elif choice == 7:
            print("Please enter the cost of the bill: ")
            bill = float(input("> "))
            print(" ")
            print("Would you like to split the bill evenly or based on total balance?")
            print("1. Split evenly")
            print("2. Split based on total balance")
            split_choice = int(input("> "))
            if split_choice == 1:
                split_even(bill)
            elif split_choice == 2:
                print("Who will the bill be split between?")
                extract_list = user_list()
                user1 = input("User 1: ")
                user2 = input("User 2: ")
                if user1 and user2 in extract_list:
                    print(f"{user1} amount owed: {split_percent(bill, user1, user2)[0]}\n")
                    print(f"{user2} amount owed: {split_percent(bill, user1, user2)[1]}\n")
                else:
                    print("Error: One or more users is not found")  
            else:
                print("Error: Item not found")

        elif choice == 8:
            print("Please enter the amount you would like to receive a low balance warning:")
            warning = float(input("> "))
            print(f"The new low balance warning will occur when balances are at or below ${warning}")

        else:
            print("ERROR: Input is not valid")



if __name__ == "__main__":
    main()