import pandas as pd

class Bank_account:
    # Class-level variables
    bank_db = pd.DataFrame(columns=['First_name', 'Last_name', 'Password', 'Email', 'Balance'])
    bank_db.index.name = 'Account_number'
    next_account_number = 1000000  # Keeps track of the next account number

    def __init__(self, first_name: str, last_name: str, email: str, password: str, deposit: int):
        # Validation check
        parameters = [first_name, last_name, email, password]
        for i in parameters:
            assert type(i) == str, f'{i} is not a string'
        assert deposit > 0, f'The deposit needs to be greater than 0'
        
        # Assign instance variables
        self.txn_number = 1
        self.account_number = Bank_account.next_account_number

        # Assign the account number and user details
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.balance = deposit
        self.txn_database = pd.DataFrame(columns= ['Transaction number','Type of transaction','Amount','Balance'])
        txn = pd.DataFrame([{
            'Transaction number': self.txn_number,
            'Type of transaction' : 'Deposit',
            'Amount' : deposit,
            'Balance' : deposit
        }])
        
        self.txn_database = pd.concat([self.txn_database, txn], ignore_index=True)

        # Increment the account number for the next account and txn for next txn
        Bank_account.next_account_number += 1
        self.txn_number += 1

        # Add new row to the DataFrame
        new_row = pd.DataFrame({
            'First_name': [self.first_name],
            'Last_name': [self.last_name],
            'Password': [self.password],
            'Email': [self.email],
            'Balance': [self.balance]
        }, index=[self.account_number])

        Bank_account.bank_db = pd.concat([Bank_account.bank_db, new_row])

    def add_money(self, add_amount: int):
        self.balance += add_amount
        Bank_account.bank_db.at[self.account_number, 'Balance'] = self.balance
        txn = pd.DataFrame([{
            'Transaction number': self.txn_number,
            'Type of transaction' : 'Deposit',
            'Amount' : add_amount,
            'Balance' : self.balance
        }])
        self.txn_database = pd.concat([self.txn_database, txn], ignore_index=True)
        self.txn_number += 1

    def withdraw_money(self, withdraw_amount: int):
        if withdraw_amount <= self.balance:
            self.balance -= withdraw_amount
            Bank_account.bank_db.at[self.account_number, 'Balance'] = self.balance
            txn = pd.DataFrame([{
                'Transaction number': self.txn_number,
                'Type of transaction' : 'Withdrawl',
                'Amount' : withdraw_amount,
                'Balance' : self.balance
            }])
            self.txn_database = pd.concat([self.txn_database, txn], ignore_index=True)
            self.txn_number += 1
        else:
            print("Insufficient balance!")

    def check_balance(self):
        return self.balance
    
    def get_txns(self):
        return self.txn_database
    
    @classmethod
    def all_accounts(cls):
        print(cls.bank_db)

    @classmethod
    def read_all_records(cls):
        pass

class Saving_account(Bank_account):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, deposit: int):
        super().__init__(first_name, last_name, email, password, deposit)

    def withdraw_money(self, withdraw_amount: int):
        fee = 2  # Savings accounts have a fee
        total_withdraw = withdraw_amount + fee
        if total_withdraw <= self.balance:
            self.balance -= total_withdraw
            Bank_account.bank_db.at[self.account_number, 'Balance'] = self.balance
        else:
            print("Insufficient balance!")