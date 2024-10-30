import tkinter as tk
import ttkbootstrap as ttk
import bank_class as bc  # Assuming your Bank_account class is in bank_class.py
from Database_cred_and_func import conn,save_account_to_db,save_transaction_to_db,get_account_details

# Initialize all global variables
account_details = {}
account = None
txn_table = None

# Initialize App
App = ttk.Window(themename='journal')
App.title('RCB Desktop Banking App')
App.geometry('500x500')

#temp dataframe for sign_up

# Initialize variables AFTER initializing the root window
input_first_name = tk.StringVar()
input_last_name = tk.StringVar()
input_email_address = tk.StringVar()
input_password = tk.StringVar()
input_deposit = tk.StringVar()
lg_email_address = tk.StringVar()
lg_account_number = tk.StringVar()  # Now login uses account number instead of email
lg_password = tk.StringVar()
Wd_input = tk.StringVar()
ad_input = tk.StringVar()
table = None

# Function to change pages
def show_frame(frame_to_show, frame_to_hide):
    frame_to_hide.pack_forget()  # Hide the current frame
    frame_to_show.pack(fill="both", expand=True)

# Function to handle user input and actions
def handle_inputs(action, next_page, prev_page, **inputs):
    # Dynamically retrieve values based on input fields
    first_name = inputs.get('first_name').get() if inputs.get('first_name') else None
    last_name = inputs.get('last_name').get() if inputs.get('last_name') else None
    email = inputs.get('email').get() if inputs.get('email') else None
    password = inputs.get('password').get() if inputs.get('password') else None
    deposit = int(inputs.get('deposit').get()) if inputs.get('deposit') else None
    account_type = inputs.get('account_type').get() if inputs.get('account_type') else None
    withdraw_input = int(inputs.get('withdraw_input').get()) if inputs.get('withdraw_input') else None
    add_funds_input = int(inputs.get('add_funds_input').get()) if inputs.get('add_funds_input') else None
    table = inputs.get('table')

    # Accessing global variables
    global account
    global account_details
    global txn_table

    if action == 'create_account':
        if account_type == "Current Account":
            save_account_to_db(first_name, last_name, email, password, deposit,'Current_Account')
        elif account_type == "Savings Account":
            save_account_to_db(first_name, last_name, email, password, deposit,'Saving_account')

        # Update the button to go to home page after sign-up
        confirmation_button.config(text='Go to homepage', command=lambda: show_frame(home_page, confirmation))
        confirmation_text.config(text=f'Congratulations {first_name}! You have successfully opened a {account_type}. Your balance is {deposit}')
        show_frame(next_page, prev_page)
    
    elif action == 'sign_in':
        account_details = get_account_details(email,password)
        if not account_details :
            lg_try_again.config(text="Account number or password incorrect. Please try again.")
            lg_try_again.pack()
        else:
            if account_details['account_type'] == 'Current_Account' :
                account = bc.Bank_account(account_details['first_name'],account_details['last_name'],account_details['email'],account_details['password'],account_details['balance'])
            elif account_details['account_type'] == 'Saving_account' :
                account = bc.Saving_account(account_details['first_name'],account_details['last_name'],account_details['email'],account_details['password'],account_details['balance'])
            show_frame(menu_page, prev_page)

    elif action == 'Withdraw':
            account.withdraw_money(withdraw_input)
            confirmation_button.config(text='Go to menu', command=lambda: show_frame(menu_page, confirmation))
            confirmation_text.config(text=f'You have withdrawn {withdraw_input}. Your new balance is {account.balance}')
            show_frame(next_page, prev_page)

    elif action == 'add_funds':
            account.add_money(add_funds_input)
            confirmation_button.config(text='Go to menu', command=lambda: show_frame(menu_page, confirmation))
            confirmation_text.config(text=f'You have added {add_funds_input}. Your new balance is {account.balance}')
            show_frame(next_page, prev_page)

    elif action == 'Show_txn':
        table = account.get_txns()
        display_transactions(table,txn_table)
        show_frame(next_page, prev_page)
    
    elif action == 'log_out':
        account = None
        show_frame(next_page, prev_page)

# Function to display the transaction table
def display_transactions(table,txn_table):

    # Insert rows into the Treeview
    for _, row in table.iterrows():
        txn_table.insert("", "end", values=list(row))

    # Pack the Treeview widget to fill the window
    txn_table.pack(fill=tk.BOTH, expand=True)


# Function to display the balance of the logged-in user
def display_balance():
    # Assuming the user's email is stored globally once logged in
    if account:
        bal_value.config(text=f"${account.balance}")

# Initialize home page and its widgets
home_page = ttk.Frame(master=App)
hp_text = ttk.Label(master=home_page, text='Welcome to Canada\'s largest banking app')
login_button = ttk.Button(master=home_page, text='Log In',command=lambda: show_frame(login_page, home_page))
sign_up_button = ttk.Button(master=home_page, text='Sign up', command=lambda: show_frame(sign_up_page, home_page))

# Pack items on the home page
home_page.pack(fill='both', expand=True)
hp_text.pack()
login_button.pack()
sign_up_button.pack()

# Initialize sign up page
sign_up_page = ttk.Frame(master=App)
su_main_text = ttk.Label(master=sign_up_page, text='Please enter details below')
su_first_name_text = ttk.Label(master=sign_up_page, text='First Name')
su_first_name_input = ttk.Entry(sign_up_page, textvariable=input_first_name, justify='center')
su_last_name_text = ttk.Label(master=sign_up_page, text='Last Name')
su_last_name_input = ttk.Entry(sign_up_page, textvariable=input_last_name, justify='center')
su_email_text = ttk.Label(master=sign_up_page, text='Email Address')
su_email_input = ttk.Entry(sign_up_page, textvariable=input_email_address, justify='center')
su_password_text = ttk.Label(master=sign_up_page, text='Password')
su_password_input = ttk.Entry(sign_up_page, textvariable=input_password, show="*", justify='center')
su_deposit_text = ttk.Label(master=sign_up_page, text='Please enter the initial deposit amount')
su_deposit_input = ttk.Entry(sign_up_page, textvariable=input_deposit, justify='center')
su_type_text = ttk.Label(master=sign_up_page, text='Type of account')
su_type_input = ttk.Combobox(master=sign_up_page, state="readonly", values=["Current Account", "Savings Account"])
su_button = ttk.Button(sign_up_page, text='Submit', 
    command=lambda:handle_inputs(
        'create_account',
        confirmation,  # Page to show
        sign_up_page,          # Page to hide
        first_name=input_first_name, 
        last_name=input_last_name, 
        email=input_email_address, 
        password=input_password, 
        deposit=input_deposit, 
        account_type=su_type_input
))

# Pack items to sign-up page
su_main_text.pack()
su_first_name_text.pack()
su_first_name_input.pack()
su_last_name_text.pack()
su_last_name_input.pack()
su_email_text.pack()
su_email_input.pack()
su_password_text.pack()
su_password_input.pack()
su_deposit_text.pack()
su_deposit_input.pack()
su_type_text.pack()
su_type_input.pack()
su_button.pack()

# confirmation page
confirmation = ttk.Frame(master=App)
confirmation_text = ttk.Label(confirmation, text='')  # Placeholder text
# Confirmation page button (initially set to go to the home page)
confirmation_button = ttk.Button(confirmation, text='', command='')

# Pack items on sign-up confirmation page
confirmation_text.pack()
confirmation_button.pack()

# Login page
login_page = ttk.Frame(master=App)
lg_email_text = ttk.Label(master=login_page, text='Email Adress')
lg_email_input = ttk.Entry(login_page, textvariable=lg_email_address, justify='center')
lg_password_text = ttk.Label(master=login_page, text='Password')
lg_password_input = ttk.Entry(login_page, textvariable=lg_password,show='*', justify='center')
lg_button = ttk.Button(login_page, text='Sign in', command=lambda: 
    handle_inputs(
        'sign_in',
        menu_page,          # Page to show
        login_page,         # Page to hide
        email=lg_email_address, 
        password=lg_password
))
lg_try_again = ttk.Label(master=login_page, text='Please try again email or password incorrect')


# Pack items on login page
lg_email_text.pack()
lg_email_input.pack()
lg_password_text.pack()
lg_password_input.pack()
lg_button.pack()

# menu page
menu_page = ttk.Frame(master=App)
menu_text = ttk.Label(master=menu_page, text='Welcome')
menu_button_withdraw = ttk.Button(menu_page, text='Withdraw', command=lambda : show_frame(Withdraw_Page,menu_page))
menu_button_add_funds = ttk.Button(menu_page, text='Add Funds', command=lambda : show_frame(Add_Funds_Page,menu_page))
menu_button_balance = ttk.Button(menu_page, text='Balance', command=lambda : show_frame(Balance_page,menu_page))
menu_button_txn = ttk.Button(menu_page, text='Transactions', command=lambda : 
      handle_inputs(
        'Show_txn',
        Txns_page,          # Page to show
        menu_page,         # Page to hide
        table=txn_table
))
menu_log_out_button = ttk.Button(menu_page, text='Log Out', command=lambda : 
      handle_inputs(
        'log_out',
        home_page,          # Page to show
        menu_page        # Page to hide
))

#Pack items on menu
menu_text.pack()
menu_button_withdraw.pack()
menu_button_add_funds.pack()
menu_button_balance.pack()
menu_button_txn.pack()
menu_log_out_button.pack(side = 'bottom')

#withdraw page
Withdraw_Page = ttk.Frame(master=App)
W_text = ttk.Label(master=Withdraw_Page, text='Please enter amount to withdraw')
W_input = ttk.Entry(Withdraw_Page, textvariable= Wd_input, justify='center')
W_button = ttk.Button(Withdraw_Page, text='Withdraw', command=lambda: 
    handle_inputs(
        'Withdraw',
        confirmation,  # Page to show
        Withdraw_Page,         # Page to hide
        withdraw_input = Wd_input
    ))

#pack withdraw page
W_text.pack()
W_input.pack()
W_button.pack()

# Add_Funds_Page
Add_Funds_Page = ttk.Frame(master=App)
af_main_text = ttk.Label(master=Add_Funds_Page, text="Enter amount to add to your account")
af_input = ttk.Entry(Add_Funds_Page, textvariable=ad_input, justify='center')
af_button = ttk.Button(Add_Funds_Page, text='Add Funds', command=lambda: 
    handle_inputs(
        'add_funds',
        confirmation,  # Page to show after adding funds
        Add_Funds_Page,        # Page to hide
        add_funds_input =ad_input
    ))


# Pack items on Add_Funds_Page
af_main_text.pack()
af_input.pack()
af_button.pack()

# Balance_page
Balance_page = ttk.Frame(master=App)
bal_main_text = ttk.Label(master=Balance_page, text="Your current balance is:")
bal_value = ttk.Label(master=Balance_page, text='')  # Placeholder for the balance value

# Button to check balance and display it
bal_button = ttk.Button(Balance_page, text='Show Balance', command=display_balance)
bal_confirmation_button = ttk.Button(Balance_page,text='Go to homepage', command=lambda: show_frame(menu_page, Balance_page))

# Pack items on Balance_page
bal_main_text.pack()
bal_value.pack()
bal_button.pack()
bal_confirmation_button.pack()

# Txns_page
Txns_page = ttk.Frame(master=App)
txn_table = ttk.Treeview(Txns_page, columns=('Transaction Number', 'Description', 'Amount'), show='headings')
txn_table.heading('Transaction Number', text='Transaction Number')
txn_table.heading('Description', text='Description')
txn_table.heading('Amount', text='Amount')


# Center-align the columns
txn_table.column('Transaction Number', anchor='center')
txn_table.column('Description', anchor='center')
txn_table.column('Amount', anchor='center')


# Txns_page
scrollbar = ttk.Scrollbar(Txns_page, orient='vertical', command=txn_table.yview)
txn_table.configure(yscroll=scrollbar.set)
back_to_menu_button = ttk.Button(Txns_page, text="Back to Menu", command=lambda: show_frame(menu_page, Txns_page))


# pack widgets on txn page
# txn_table.pack(fill='both', expand=True, side='left')
scrollbar.pack(fill='y', side='right')
back_to_menu_button.pack(pady=10)

# run loop
App.mainloop()
