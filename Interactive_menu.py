from Bank import *

o_bank = Bank(hours="9 to 5", address="123 Main Street, Anytown, US", phone="123 123-1212")

print("\n")
print("Note the admin password is:", o_bank.admin_password)

while True:
    print()
    print("To get an account balance, press b")
    print("To close an account, press c")
    print("To make a deposit, press d")
    print("To get bank information, press i")
    print("To open a new account, press o")
    print("To quit, press q")
    print("To show all accounts, press s")
    print("To make a withdrawal, press w")
    print("To change an account password, press u")
    print("To transfer money, press t")
    print()

    action = input("What do you want to do?: ")
    action = action.lower()
    action = action[0] # grab the first letter 
    print()

    try:
        if action == "b":
            o_bank.balance()
        elif action == "c":
            o_bank.close_account()
        elif action == "d":
            o_bank.deposit()
        elif action == "i":
            o_bank.get_info()
        elif action == "o":
            o_bank.open_account()
        elif action == "q":
            o_bank.close_database_connections()
            break
        elif action == "s":
            o_bank.show()
        elif action == "w":
            o_bank.withdraw()
        elif action == "u":
            o_bank.update_account_password()
        elif action == "t":
            o_bank.transfer_to()
    except AbortTransaction as error:
        print(error)

print("Done")