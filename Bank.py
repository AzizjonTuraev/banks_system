from Accounts import *
import sqlite3
import datetime

class Bank():
    
    def __init__(self, hours, address, phone, accounts_database_name="accounts_database.db", bank_name = "Bank_branch_name",
                 transaction_database_name = "transaction_database.db", admin_password = "password"):
        self.bank_name = bank_name
        self.account_dict = {}
        self.accounts_database_name = accounts_database_name
        self.transaction_database_name = transaction_database_name
        self.hours = hours
        self.address = address
        self.phone = phone
        self.accounts_conn = None
        self.accounts_cursor = None
        self.transactions_conn = None
        self.transactions_cursor = None
        self.connect_to_account_database()
        self.connect_to_transactions_database()
        self.fetch_accounts_data()
        self.admin_password = admin_password
        self.next_account_number = self.get_the_last_customer_id()


    def ask_for_valid_account_number(self):
        account_number = input("Please, enter your account number: ")
        try:
            account_number = int(account_number)
        except ValueError:
            raise AbortTransaction("The account number must be an integer")
        if account_number not in self.account_dict:
            raise AbortTransaction("There is no account with account number:", str(account_number))
        return account_number


    def ask_for_valid_password(self, o_account):
        password = input("Please, enter your password: ")
        o_account.check_password_match(password)


    def get_user_account(self):
        account_number = self.ask_for_valid_account_number()
        o_account = self.account_dict[account_number]
        self.ask_for_valid_password(o_account)
        return o_account

    
    def create_account(self, username, password, currency, starting_amount):
        o_account = Accounts(self.next_account_number, username, password, currency, starting_amount)
        new_account_number = self.next_account_number
        self.account_dict[new_account_number] = o_account
        self.next_account_number = self.next_account_number + 1 
        try:
            self.save_to_accounts_database(o_account)
            self.save_to_transactions_database_debit(o_account, starting_amount, "account opening", None, "open account")
            return new_account_number
        except:
            raise AbortTransaction("The account has not been created. Please check for the correctness of the inputs")



    def open_account(self):
        print("*** Open Account ***")
        username = input("Please enter create an username: ")
        user_currency = input("Please, enter the type of currency you want to deposit on your account: " )
        user_starting_amount = float(input("Please, enter the amount of money you want to deposit on your account: "))
        user_password = input("Please create a password: ")
        user_account_number = self.create_account(username, user_password, user_currency, user_starting_amount)
        print("Your account number is", user_account_number)

    
    def close_account(self):
        print("*** Close Account ***")
        user_account_number = self.ask_for_valid_account_number()
        o_account = self.account_dict[user_account_number]
        self.ask_for_valid_password(o_account)
        the_balance = o_account.get_balance()
        the_currency = o_account.get_currency()
        print(f"You have {the_balance} {the_currency} amount of money in your account, which is going to be returned to you")
        self.close_account_status(o_account)
        self.save_to_transactions_database_credit(o_account, the_balance, "account closing", None, "close account")
        del self.account_dict[user_account_number]
        print("Your account is now closed")


    def balance(self):
        print("*** Get Balance ***")
        o_account = self.get_user_account()
        print(o_account)
        the_balance = o_account.get_balance()
        the_currency = o_account.get_currency()
        print("Your account balance is:", the_balance, the_currency)


    def deposit(self):
        print("*** Deposit ***")
        o_account = self.get_user_account()
        account_id = o_account.account_id
        amount_to_deposit = input("Please, enter amount to deposit: ")
        the_balance = o_account.deposit(amount_to_deposit)
        the_currency = o_account.get_currency()
        print("Deposited:", amount_to_deposit, the_currency)
        print("Your new balance is:", the_balance, the_currency)
        self.update_balance_increase(amount_to_deposit, account_id)
        self.save_to_transactions_database_debit(o_account, amount_to_deposit, "deposit", None, "deposit")


    def update_balance_increase(self, amount, account_id):
        # Update the SQL database
        self.accounts_cursor.execute('''
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_id = ?
        ''', (amount, account_id))
        # Commit the changes to the accounts database
        self.accounts_conn.commit()


    def update_balance_decrease(self, amount, account_id):
        # Update the SQL database
        self.accounts_cursor.execute('''
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_id = ?
        ''', (amount, account_id))
        # Commit the changes to the accounts database
        self.accounts_conn.commit()

    
    def withdraw(self):
        print("*** Withdraw ***")
        o_account = self.get_user_account()
        account_id = o_account.account_id
        amount_to_withdraw = input("Please enter the amount to withdraw: ")
        the_balance = o_account.withdraw(amount_to_withdraw)
        the_currency = o_account.get_currency()
        print("Withdrew:", amount_to_withdraw, the_currency)
        print("Your new balance:", the_balance, the_currency)
        self.update_balance_decrease(amount_to_withdraw, account_id)
        self.save_to_transactions_database_credit(o_account, amount_to_withdraw, "withdraw money", None, "withdraw")


    def get_info(self):
        print("Bank name", self.bank_name)
        print("Hours:", self.hours)
        print("Address:", self.address)
        print("Phone:", self.phone)
        print(f"We currently have {len(self.account_dict)} accounts open")

    
    def show(self):
        print("*** Show ***")
        print("*** This would typically require an admin password")
        print("*** Enter x, if you want to terminate the function")
        while True:
            entered_password = input("Please, enter the admin password: ")
            if entered_password == self.admin_password:
                if len(self.account_dict):
                    for user_account_number in self.account_dict:
                        o_account = self.account_dict[user_account_number]
                        print("\n Account:", user_account_number)
                        o_account.show()
                else:
                    print("\n We dont have any customers yet in our database:", self.accounts_database_name)
                
                break
            elif entered_password == "x":
                break


    def connect_to_account_database(self):
        # Connect to the SQLite database for accounts
        self.accounts_conn = sqlite3.connect(self.accounts_database_name)
        self.accounts_cursor = self.accounts_conn.cursor()
        # Create a table for accounts if it doesn't exist
        self.accounts_cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY,
                account_holder_name TEXT,
                password TEXT,
                currency TEXT,
                balance REAL,
                account_status TEXT
            )
        ''')


    def connect_to_transactions_database(self):
        # Connect to the SQLite database for transactions
        self.transactions_conn = sqlite3.connect(self.transaction_database_name)
        self.transactions_cursor = self.transactions_conn.cursor()
        # Create a table for transactions if it doesn't exist
        self.transactions_cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER,
                account_id INTEGER,
                debit REAL,
                credit REAL,
                reason TEXT,
                receiver_id INTEGER,
                transaction_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')


    def fetch_accounts_data(self):
        # Fetch account data from the accounts database
        self.accounts_cursor.execute('SELECT * FROM accounts')
        accounts_data = self.accounts_cursor.fetchall()

        # Populate the account_dict with Account instances
        for account_data in accounts_data:
            account_id, account_holder_name, password, currency, balance, account_status = account_data
            if account_status == "active":
                account = Accounts(account_id, account_holder_name, password, currency, balance)
                self.account_dict[account_id] = account


    def get_the_last_customer_id(self):
        self.accounts_cursor.execute('SELECT account_id FROM accounts')
        accounts_data = self.accounts_cursor.fetchall()
        return len(accounts_data)


    def save_to_accounts_database(self, account):
        # Insert account data into the database
        self.accounts_cursor.execute('''
                INSERT INTO accounts (account_id, account_holder_name, password, currency, balance, account_status)
                VALUES (?, ?, ?, ?, ?, ?)
        ''', (account.account_id, account.username, account.password, account.currency, account.balance, "active"))
        # Commit the changes
        self.accounts_conn.commit()


    def save_to_transactions_database_debit(self, account_id, debit_amount, reason, receiver_id, transaction_type):
        # Insert account data into the database
        if account_id.__class__ == Accounts:        
            account_id = account_id.account_id
        if receiver_id.__class__ == Accounts:
            receiver_id = receiver_id.account_id

        self.transactions_cursor.execute('''
                INSERT INTO transactions (transaction_id, 
                                         account_id, 
                                         debit, 
                                         credit, 
                                         reason, 
                                         receiver_id,
                                         transaction_type,
                                         timestamp
                                         )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), 
              account_id, 
              debit_amount, 
              0, 
              reason, 
              receiver_id, 
              transaction_type, 
              datetime.datetime.now()))
        # Commit the changes
        self.transactions_conn.commit()


    def save_to_transactions_database_credit(self, account_id, credit_amount, reason, receiver_id, transaction_type):
        # Insert account data into the database
        if account_id.__class__ == Accounts:        
            account_id = account_id.account_id
        if receiver_id.__class__ == Accounts:
            receiver_id = receiver_id.account_id
        self.transactions_cursor.execute('''
                INSERT INTO transactions (transaction_id, 
                                         account_id, 
                                         debit, 
                                         credit, 
                                         reason, 
                                         receiver_id,
                                         transaction_type,
                                         timestamp
                                         )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), 
              account_id, 
              0, 
              credit_amount, 
              reason, 
              receiver_id, 
              transaction_type, 
              datetime.datetime.now()))
        # Commit the changes
        self.transactions_conn.commit()



    def close_database_connections(self):
        # Close the connections to both databases
        if self.accounts_conn:
            self.accounts_conn.close()
        if self.transactions_conn:
            self.transactions_conn.close()


    def update_account_password(self):
        o_account = self.get_user_account()
        new_password = input("Please, enter the new password: ")
        account_id = o_account.account_id
        # Update the SQL database
        self.accounts_cursor.execute('''
            UPDATE accounts
            SET password = ?
            WHERE account_id = ?
        ''', (new_password, account_id))
        # Commit the changes to the accounts database
        self.accounts_conn.commit()
        self.account_dict[account_id].password = new_password


    def close_account_status(self, o_account):
        account_id = o_account.account_id
        # Update the SQL database
        self.accounts_cursor.execute('''
            UPDATE accounts
            SET account_status = ?,
            balance = ?
            WHERE account_id = ?
        ''', ("closed", 0, account_id))
        # Commit the changes to the accounts database
        self.accounts_conn.commit()

    
    def transfer_to(self):
        print("*** Tranfer to ***")
        o_account = self.get_user_account()
        sender_account_id = o_account.account_id
        transfer_amount_currency = o_account.currency
        receiver_id = int(input("Please, enter the receiver account id: "))
        transfer_amount = float(input("Please, enter the amount of money you want to transfer: "))
        reason = input("Please, enter the purpose of the transfer: ")
        if receiver_id in self.account_dict.keys():
            receiver_currency = self.account_dict[receiver_id].currency
            if receiver_currency != transfer_amount_currency:
                print("You are transfering money from", transfer_amount_currency, "account to", receiver_currency, "account!")
                raise AbortTransaction("You cant transfer money between different account currency types")
        the_balance = o_account.transfer_to(transfer_amount)
        print("Transferred:", transfer_amount, transfer_amount_currency)
        print("Your new balance:", the_balance, transfer_amount_currency)
        self.update_balance_decrease(transfer_amount, sender_account_id)
        self.save_to_transactions_database_credit(o_account, transfer_amount, reason, receiver_id, "transfer")
        if receiver_id in self.account_dict.keys():
            self.transfer_from(receiver_id, transfer_amount, reason, sender_account_id)


    def transfer_from(self, receiver_id, transfer_amount, reason=None, sender_account_id = None):
        self.update_balance_increase(transfer_amount, receiver_id)
        self.account_dict[receiver_id].balance = self.account_dict[receiver_id].balance + transfer_amount
        self.save_to_transactions_database_debit(receiver_id, transfer_amount, reason, sender_account_id, "transfer")
