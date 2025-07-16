from tkinter import *
import datetime

class BankSystem:
    def __init__(self, username, password, balance=0.0):
        self.username = username
        self.password = password
        self.balance = balance
        self.transactions = []

    def authenticate(self, user, pwd):
        return user == self.username and pwd == self.password

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append((datetime.datetime.now(), f"Deposited ₦{amount:.2f}"))

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.transactions.append((datetime.datetime.now(), f"Withdrew ₦{amount:.2f}"))
        return "Success"

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions


class BankSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank System GUI")

        self.bank = BankSystem("admin", "1234", 10000)

        self.login_screen()

    def login_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        Label(self.master, text="Username").pack()
        self.username_entry = Entry(self.master)
        self.username_entry.pack()

        Label(self.master, text="Password").pack()
        self.password_entry = Entry(self.master, show='*')
        self.password_entry.pack()

        Button(self.master, text="Login", command=self.login).pack()
        self.message_label = Label(self.master, text="")
        self.message_label.pack()

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if self.bank.authenticate(user, pwd):
            self.menu_screen()
        else:
            self.message_label.config(text="Login failed", fg="red")

    def menu_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        Label(self.master, text="Welcome to Kinsley Bank System", font=("Arial", 14)).pack(pady=10)

        Button(self.master, text="Deposit", bg='red',command=self.deposit_screen).pack(pady=5)
        Button(self.master, text="Withdraw", bg='green',command=self.withdraw_screen).pack(pady=5)
        Button(self.master, text="Check Balance", bg='blue',command=self.check_balance).pack(pady=5)
        Button(self.master, text="Transaction History", bg='yellow',command=self.view_transactions).pack(pady=5)
        Button(self.master, text="Logout", command=self.login_screen).pack(pady=5)

        self.output_label = Label(self.master, text="")
        self.output_label.pack(pady=10)

    def deposit_screen(self):
        amount = self.popup_input("Enter amount to deposit:")
        if amount:
            try:
                self.bank.deposit(float(amount))
                self.output_label.config(text=f"Deposited ₦{amount}")
            except ValueError:
                self.output_label.config(text="Invalid amount!")

    def withdraw_screen(self):
        amount = self.popup_input("Enter amount to withdraw:")
        if amount:
            try:
                result = self.bank.withdraw(float(amount))
                if result == "Success":
                    self.output_label.config(text=f"Withdrew ₦{amount}")
                else:
                    self.output_label.config(text="Insufficient funds")
            except ValueError:
                self.output_label.config(text="Invalid amount!")

    def check_balance(self):
        balance = self.bank.get_balance()
        self.output_label.config(text=f"Current balance: ₦{balance:.2f}")

    def view_transactions(self):
        transactions = self.bank.get_transactions()
        if not transactions:
            self.output_label.config(text="No transactions yet.")
        else:
            history = "\n".join([f"{t[0].strftime('%Y-%m-%d %H:%M:%S')} - {t[1]}" for t in transactions])
            self.popup_message("Transaction History", history)

    def popup_input(self, prompt):
        top = Toplevel(self.master)
        top.title("Input")

        Label(top, text=prompt).pack(pady=5)
        entry = Entry(top)
        entry.pack(pady=5)
        result = []

        def submit():
            result.append(entry.get())
            top.destroy()

        Button(top, text="OK", command=submit).pack(pady=5)
        self.master.wait_window(top)
        return result[0] if result else None

    def popup_message(self, title, message):
        top = Toplevel(self.master)
        top.title(title)
        Label(top, text=message, justify=LEFT).pack(pady=10, padx=10)
        Button(top, text="Close", command=top.destroy).pack(pady=5)


root = Tk()
app = BankSystemGUI(root)
root.mainloop()


