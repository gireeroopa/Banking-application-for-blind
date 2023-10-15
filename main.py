import tkinter as tk
from tkinter import messagebox
import time
import os




import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="194.59.164.85",
    user="u738796213_blindapp",
    password="Blindapp!@1",
    database="u738796213_blindapp"
)

# Check if the connection was successful
if db.is_connected():
    print("Connected to the MySQL database!")

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create the bank_accounts table if it doesn't exist
#cursor.execute("CREATE TABLE IF NOT EXISTS bank_accounts (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), balance FLOAT)")

# Insert some test data into the bank_accounts table
#cursor.execute("INSERT INTO bank_accounts (name, balance) VALUES ('John', 1000)")

# Commit the changes to the database
#db.commit()

# Fetch all the rows from the bank_accounts table
cursor.execute("SELECT * FROM bank_accounts")





class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
          print(row[2])
          self.balance = int(row[2])
        
    def deposit(self, amount):
        self.balance += amount
        cursor.execute("INSERT INTO bank_accounts (name, balance) VALUES (%s, %s)", ("John", self.balance))
        db.commit()

    def withdraw(self, amount):
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            self.balance -= amount
            cursor.execute("INSERT INTO bank_accounts (name, balance) VALUES (%s, %s)", ("John", self.balance))
            db.commit()
            messagebox.showinfo("Success", "Withdrawal successful.")
            
    def get_balance(self):
        
        return self.balance

class BrailleKeyboard(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.entries = []
        self.bank_account = BankAccount("John", 1000)
        self.create_widgets()
        self.prev_button = None
        self.select = 0
        self.value = ""

    def set_entry(self, *entries):
        self.entries = entries
        for entry in self.entries:
            entry.config(state=tk.NORMAL)
        
    def create_widgets(self):
        # Create buttons for each dot combination
        buttons = [
            {"text": "⠁", "dots": "1"},
            {"text": "⠁", "dots": "2"},
            {"text": "⠁", "dots": "3"},
            {"text": "⠁", "dots": "4"},
            {"text": "⠁", "dots": "5"},
            {"text": "⠁", "dots": "6"},
            {"text": "⠁", "dots": "7"},
            {"text": "⠁", "dots": "8"},
        ]
        
                # Create buttons and place them on the frame
        for button in buttons:
            btn = tk.Button(self, text=button["text"], width=5, height=2, font=("Arial", 16), command=lambda dots=button["dots"]: self.on_button_click(dots))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def on_button_click(self, dots):
        # Add the dots to the entry field
        curr_button = dots
        curr_time = time.time()
        if self.prev_button is not None and curr_time - self.prev_time <= 1.5:
            # If the current button is clicked within 0.5 seconds of the previous button, append it to the previous button's dots
            combined_dots = self.prev_button + curr_button
            digit = self.dots_to_digit(combined_dots)
            if digit is not None:
             if self.select == 0:
                print("login")
                if len(self.value)<6:
                    self.entries[0].insert(tk.END, digit)
                else:
                    self.entries[1].insert(tk.END, digit)
                #self.entry.insert(tk.END, digit)
                self.value += digit
                print(self.value)
             else:
                   print("select")
                   if digit == "1":
                        print("balance")
                            # Show the account balance
                        balance = self.bank_account.get_balance()
                        messagebox.showinfo("Account Balance", f"Your balance is {balance}.")
                        data = "your balance is" + str(balance)
                   elif digit == "2":
                        print("deposit")
                            # Show the account balance
                        self.bank_account. deposit(100)
                        balance = self.bank_account.get_balance()
                        messagebox.showinfo("100 Credited", f"Your balance is {balance}.")
                   elif digit == "3":
                        print("withdraw")
                            # Show the account balance
                        self.bank_account.withdraw(500)
                        balance = self.bank_account.get_balance()
                        messagebox.showinfo("500 Debited", f"Your balance is {balance}.")
        
                       
            self.prev_button = None
        else:
            # If the current button is clicked more than 0.5 seconds after the previous button, add its dots to the entry field
            digit = self.dots_to_digit(curr_button)
            #if digit is not None:
             #   self.entry.insert(tk.END, digit)
            self.prev_button = curr_button
            self.prev_time = curr_time
            
    def dots_to_digit(self, dots):
        print(dots)
        # Convert the dots to a digit
        if dots == "11":
            return "1"
        elif dots == "22":
            return "2"
        elif dots == "33":
            return "3"
        elif dots == "44":
            return "4"
        elif dots == "55":
            return "5"
        elif dots == "66":
            return "6"
        elif dots == "77":
            return "7"
        elif dots == "88":
            return "8"
        elif dots == "14":
            return "9"
        elif dots == "78":
            return "0"
        elif dots == "56":
            return " "
        else:
            return None

class BankApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Braille Bank App")
        # Set the window size and allow resizing
        self.geometry("800x600")
        self.resizable(True, True)

        # Create the entry fields for the account and pin
        self.account_entry = tk.Entry(self, font=("Arial", 16), width=25)
        self.pin_entry = tk.Entry(self, font=("Arial", 16), width=25, show="*")
        
        # Create the buttons for the login and exit actions
        self.login_button = tk.Button(self, text="Login", width=10, height=2, font=("Arial", 16), command=self.login)
        self.exit_button = tk.Button(self, text="Exit", width=10, height=2, font=("Arial", 16), command=self.exit_app)
        
        # Place the entry fields and buttons on the frame
        self.account_entry.place(x=50, y=200)
        self.pin_entry.place(x=50, y=250)
        self.login_button.place(x=50, y=300)
        self.exit_button.place(x=300, y=300)
        
        # Hide the entry fields and buttons until the user is authenticated
        #self.hide_widgets()
        
        # Create the Braille keyboard widget and place it on the frame
        self.braille_keyboard = BrailleKeyboard(self)
        self.braille_keyboard.pack(padx=10, pady=10)

        self.braille_keyboard.set_entry(self.account_entry, self.pin_entry)
        
        
        # Initialize the account and pin variables
        self.account = None
        self.pin = None
	
        
    def hide_widgets(self):
        print("hide widget")
        self.account_entry.place_forget()
        self.pin_entry.place_forget()
        self.login_button.place_forget()
        self.exit_button.place_forget()
        
    def show_widgets(self):
        self.account_entry.pack(padx=10, pady=10)
        self.login_button.pack(padx=10, pady=10, side=tk.LEFT)
        self.exit_button.pack(padx=10, pady=10, side=tk.LEFT)
    
    def login(self):
        # Get the account and pin entered by the user
        account = self.account_entry.get()
        pin = self.pin_entry.get()
        print(account, pin)
        # Authenticate the user
        self.braille_keyboard.entries[0].delete(0, tk.END)
        self.braille_keyboard.entries[1].delete(0, tk.END)
        self.braille_keyboard.value = ""
        if self.authenticate_user(account, pin):
            #self.hide_widgets()
            self.braille_keyboard.select = 1 
            # Show the account balance
            #balance = self.account.get_balance()
            #messagebox.showinfo("Account Balance", f"Your balance is {balance}.")
        
            # Show the Braille keyboard and hide the login widgets
            
            self.braille_keyboard.pack(padx=10, pady=10)
            # Add this line to hide the login widgets after authentication
            self.hide_widgets()
            #self.show_main_menu()
        else:
            # If the user is not authenticated, show an error message
            messagebox.showerror("Error", "Invalid account or pin.")
              
    def authenticate_user(self, account_num, pin):
       # Check if the account number and pin are valid
       accounts = {"123456": "1234", "987654": "5678", "246810": "0000"}
       if account_num in accounts and accounts[account_num] == pin:
           # If the account number and pin are valid, initialize the account object
           self.account = BankAccount(account_num)
           return True
       else:
           return False
    
    def deposit(self):
       # Prompt the user to enter the deposit amount
       amount = float(tk.simpledialog.askstring("Deposit", "Enter deposit amount:"))
       if amount > 0:
           # Deposit the amount and update the balance label
           self.account.deposit(amount)
           balance_label = tk.Label(self, text="Balance: ${:.2f}".format(self.account.get_balance()), font=("Arial", 16))
           balance_label.pack(padx=10, pady=10)
       else:
           messagebox.showerror("Error", "Invalid deposit amount.")
        
    def withdraw(self):
       # Prompt the user to enter the withdrawal amount
       amount = float(tk.simpledialog.askstring("Withdrawal", "Enter withdrawal amount:"))
       if amount > 0:
           # Withdraw the amount and update the balance label
           self.account.withdraw(amount)
           balance_label = tk.Label(self, text="Balance: ${:.2f}".format(self.account.get_balance()), font=("Arial", 16))
           balance_label.pack(padx=10, pady=10)
       else:
           messagebox.showerror("Error", "Invalid withdrawal amount.")
      
    def show_main_menu(self):
       # Create the buttons for the account balance and transfer actions
        balance_button = tk.Button(self, text="Account Balance", width=20, height=2, font=("Arial", 16), command=self.show_balance)
        transfer_button = tk.Button(self, text="Transfer Funds", width=20, height=2, font=("Arial", 16), command=self.show_transfer)
            # Place the buttons on the frame
        balance_button.pack(padx=10, pady=10)
        transfer_button.pack(padx=10, pady=10)
    
    def show_balance(self):
        # Create a label with the account balance and place it on the frame
        balance_message = f"Your account balance is: ${self.get_account_balance()}"
        balance_label = tk.Label(self, text=balance_message, font=("Arial", 16))
        balance_label.pack(padx=10, pady=10)
        
    def transfer_funds(self):
        # Create the entry fields for the recipient's account and the amount to transfer
        recipient_entry = tk.Entry(self, font=("Arial", 16), width=25)
        amount_entry = tk.Entry(self, font=("Arial", 16), width=25)
        
        # Create the buttons for the transfer and cancel actions
        transfer_button = tk.Button(self, text="Transfer", width=10, height=2, font=("Arial", 16), command=lambda: self.transfer(recipient_entry.get(), amount_entry.get()))
        cancel_button = tk.Button(self, text="Cancel", width=10, height=2, font=("Arial", 16), command=self.cancel_transfer)
        
        # Place the entry fields and buttons on the frame
        recipient_entry.pack(padx=10, pady=10)
        amount_entry.pack(padx=10, pady=10)
        transfer_button.pack(padx=10, pady=10, side=tk.LEFT)
        cancel_button.pack(padx=10, pady=10, side=tk.LEFT)
        
        # Hide the main menu buttons until the transfer is complete or cancelled
        self.hide_main_menu()
        
    def hide_main_menu(self):
        for widget in self.winfo_children():
            widget.pack_forget()
        
    def show_main_menu(self):
        # Create the buttons for the account balance and transfer actions
        balance_button = tk.Button(self, text="Account Balance", width=20, height=2, font=("Arial", 16), command=self.show_balance)
        transfer_button = tk.Button(self, text="Transfer Funds", width=20, height=2, font=("Arial", 16), command=self.show_transfer)
        
        # Pack the buttons
        balance_button.pack(padx=10, pady=10)
        transfer_button.pack(padx=10, pady=10)
        
    def transfer(self, recipient, amount):
        # Check if the recipient and amount are valid
        if recipient == "" or amount == "":
            # If invalid, display an error message
            error_message = "Recipient and amount are required fields. Please try again."
            error_label = tk.Label(self, text=error_message, font=("Arial", 16), fg="red")
            error_label.pack(padx=10, pady=10)
        else:
            # If valid, transfer the funds and display a success message
            self.transfer_funds_to(recipient, float(amount))
            success_message = f"${amount} transferred to account {recipient}."
            success_label = tk.Label(self, text=success_message, font=("Arial", 16), fg="green")
            success_label.pack(padx=10, pady=10)
        
        # Reset the recipient and amount entry fields
        self.clear_transfer_fields()
        
        # Show the main menu buttons
        self.show_main_menu_buttons()
        
    def cancel_transfer(self):
        # Clear the recipient and amount entry fields
        self.clear_transfer_fields()
        
        # Show the main menu buttons
        self.show_main_menu_buttons()
        
    def show_balance(self):
        # Display the account balance
        balance_message = f"Your account balance is ${self.account_balance}."
        balance_label = tk.Label(self, text=balance_message, font=("Arial", 16))
        balance_label.pack(padx=10, pady=10)
        
    def transfer_funds(self):
        # Create the entry field for the transfer amount
        transfer_entry = tk.Entry(self, font=("Arial", 16), width=25)
        transfer_entry.pack(padx=10, pady=10)
        
        # Create the button for the transfer action
        transfer_button = tk.Button(self, text="Transfer", width=10, height=2, font=("Arial", 16), command=lambda: self.process_transfer(transfer_entry.get()))
        transfer_button.pack(padx=10, pady=10)
        
    def process_transfer(self, transfer_amount):
        # Convert the transfer amount to a float
        try:
            transfer_amount = float(transfer_amount)
        except ValueError:
            # If the transfer amount is not a valid number, display an error message and return
            error_message = "Invalid transfer amount. Please enter a valid number."
            error_label = tk.Label(self, text=error_message, font=("Arial", 16), fg="red")
            error_label.pack(padx=10, pady=10)
            return
        
        # Check if the transfer amount is greater than the account balance
        if transfer_amount > self.account_balance:
            # If the transfer amount is greater than the account balance, display an error message and return
            error_message = "Insufficient funds. Please enter a lower amount."
            error_label = tk.Label(self, text=error_message, font=("Arial", 16), fg="red")
            error_label.pack(padx=10, pady=10)
            return
        
        # If the transfer amount is valid, deduct it from the account balance
        self.account_balance -= transfer_amount
        
        # Display a success message with the new account balance
        success_message = f"Transfer of ${transfer_amount:.2f} was successful. Your new account balance is ${self.account_balance:.2f}."
        success_label = tk.Label(self, text=success_message, font=("Arial", 16))
        success_label.pack(padx=10, pady=10)
        
    def exit_app(self):
        # Close the application
        # Close the database connection
        db.close()        
        self.destroy()
        

# Create an instance of BankApp
#app = BankApp()

# Create an instance of BrailleKeyboard and pack it onto the BankApp frame
#braille_keyboard = BrailleKeyboard(app, app.account_entry)
#braille_keyboard.pack(padx=10, pady=10)

if __name__ == "__main__":
    app = BankApp()
    app.mainloop()

