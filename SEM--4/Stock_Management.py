import sqlite3
from tkinter import *
from tkinter import messagebox
def create_tables():
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT,
                        quantity INTEGER,
                        price REAL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id INTEGER PRIMARY KEY,
                        product_id INTEGER,
                        quantity INTEGER,
                        total_cost REAL,
                        transaction_type TEXT,
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                    )''')
    conn.commit()
    conn.close()
def add_product(name, quantity, price):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                   (name, quantity, price))
    conn.commit()
    conn.close()
def update_product(product_id, quantity):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE product_id = ?",
                   (quantity, product_id))
    conn.commit()
    conn.close()
def search_product(product_id):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row
def record_transaction(product_id, quantity, total_cost, transaction_type):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (product_id, quantity, total_cost, transaction_type) VALUES (?, ?, ?, ?)",
                   (product_id, quantity, total_cost, transaction_type))
    conn.commit()
    conn.close()
def display_add_product_window():
    def add_product_click():
        name = name_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
        add_product(name, quantity, price)
        add_product_window.destroy()
    add_product_window = Tk()
    add_product_window.geometry("200x150")
    add_product_window.title("Add Product")
    Label(add_product_window, text="Name:").grid(row=0, column=0)
    Label(add_product_window, text="Quantity:").grid(row=1, column=0)
    Label(add_product_window, text="Price:").grid(row=2, column=0)
    name_entry = Entry(add_product_window)
    quantity_entry = Entry(add_product_window)
    price_entry = Entry(add_product_window)
    name_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)
    price_entry.grid(row=2, column=1)
    add_button = Button(add_product_window, text="Add", command=add_product_click)
    add_button.grid(row=3, column=1)
    add_product_window.mainloop()
def display_update_product_window():
    def update_product_click():
        product_id = int(product_id_entry.get())
        quantity = int(quantity_entry.get())
        update_product(product_id, quantity)
        update_product_window.destroy()
    update_product_window = Tk()
    update_product_window.geometry("300x150")
    update_product_window.title("Update Product")
    Label(update_product_window, text="Product ID:").grid(row=0, column=0)
    Label(update_product_window, text="Quantity:").grid(row=1, column=0)
    product_id_entry = Entry(update_product_window)
    quantity_entry = Entry(update_product_window)
    product_id_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)
    update_button = Button(update_product_window, text="Update", command=update_product_click)
    update_button.grid(row=2, column=1)
    update_product_window.mainloop()
def display_search_product_window():
    def search_product_click():
        product_id = int(product_id_entry.get())
        result = search_product(product_id)
        if result:
            search_result_label.config(text=f"Name: {result[1]}, Quantity: {result[2]}, Price: {result[3]}")
        else:
            search_result_label.config(text="Product not found.")
    search_product_window = Tk()
    search_product_window.geometry("300x150")
    search_product_window.title("Search Product")
    Label(search_product_window, text="Product ID:").grid(row=0, column=0)
    product_id_entry = Entry(search_product_window)
    product_id_entry.grid(row=0, column=1)
    search_button = Button(search_product_window, text="Search", command=search_product_click)
    search_button.grid(row=1, column=1)
    search_result_label = Label(search_product_window, text="")
    search_result_label.grid(row=2, column=0, columnspan=2)
    search_product_window.mainloop()
def display_payment_window():
    def process_payment_click():
        product_id = int(prod_id_entry.get())
        quantity = int(quantity_entry.get())
        result = search_product(product_id)
        if result:
            total_cost = result[3] * quantity
            payment_confirmation = messagebox.askokcancel("Payment Confirmation",
                                                           f"Do you want to proceed with the payment of "
                                                           f"{result[1]}@okhdfcbank for ₹ {total_cost} ?")
            if payment_confirmation:
                email = email_entry.get()
                upi_id = upi_entry.get()
                messagebox.showinfo("Payment Successful", "Your payment to that merchant was successfully. "
                                                          "E-Receipt bill will be mailed to " + email)
                payment_window.destroy()
        else:
            messagebox.showerror("Error", "Product not found.")
    payment_window = Tk()
    payment_window.geometry("200x150")
    payment_window.title("Make Payment")
    Label(payment_window, text="Product ID:").grid(row=0, column=0)
    prod_id_entry = Entry(payment_window)
    prod_id_entry.grid(row=0, column=1)
    Label(payment_window, text="Quantity:").grid(row=1, column=0)
    quantity_entry = Entry(payment_window)
    quantity_entry.grid(row=1, column=1)
    Label(payment_window, text="Email Address:").grid(row=2, column=0)
    email_entry = Entry(payment_window)
    email_entry.grid(row=2, column=1)
    Label(payment_window, text="UPI ID:").grid(row=3, column=0)
    upi_entry = Entry(payment_window)
    upi_entry.grid(row=3, column=1)
    pay_button = Button(payment_window, text="Pay", command=process_payment_click)
    pay_button.grid(row=4, columnspan=2)
    payment_window.mainloop()
def display_buy_window():
    def process_buy_click():
        product_id = int(prod_id_entry.get())
        quantity = int(quantity_entry.get())
        result = search_product(product_id)
        if result:
            total_cost = result[3] * quantity
            payment_confirmation = messagebox.askokcancel("Payment Confirmation",
                                                          f"Do you want to proceed with the payment of "
                                                          f"{result[1]}@okhdfcbank for ₹ {total_cost} ?")
            if payment_confirmation:
                email = email_entry.get()
                upi_id = upi_entry.get()
                messagebox.showinfo("Payment Successful", "Your payment to that merchant was successfully. "
                                                          "E-Receipt bill will be mailed to " + email)
                buy_window.destroy()
        else:
            messagebox.showerror("Error", "Product not found.")
    buy_window = Tk()
    buy_window.geometry("200x150")
    buy_window.title("Buy Product")
    Label(buy_window, text="Product ID:").grid(row=0, column=0)
    prod_id_entry = Entry(buy_window)
    prod_id_entry.grid(row=0, column=1)
    Label(buy_window, text="Quantity:").grid(row=1, column=0)
    quantity_entry = Entry(buy_window)
    quantity_entry.grid(row=1, column=1)
    Label(buy_window, text="Email Address:").grid(row=2, column=0)
    email_entry = Entry(buy_window)
    email_entry.grid(row=2, column=1)
    Label(buy_window, text="UPI ID:").grid(row=3, column=0)
    upi_entry = Entry(buy_window)
    upi_entry.grid(row=3, column=1)
    buy_button = Button(buy_window, text="Buy", command=process_buy_click)
    buy_button.grid(row=4, columnspan=2)
    buy_window.mainloop()
def menu():
    root = Tk()
    root.geometry("200x150")
    root.title("Stock Maintenance System")
    def login_click():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin":
            root.destroy()
            admin_menu = Tk()
            admin_menu.geometry("200x150")
            admin_menu.title("Admin Portal")
            add_product_button = Button(admin_menu, text="Add Product", command=display_add_product_window)
            add_product_button.pack()
            update_product_button = Button(admin_menu, text="Update Product", command=display_update_product_window)
            update_product_button.pack()
            search_product_button = Button(admin_menu, text="Search Product", command=display_search_product_window)
            search_product_button.pack()
            payment_button = Button(admin_menu, text="Make Payment", command=display_payment_window)
            payment_button.pack()
            admin_menu.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    login_frame = Frame(root)
    login_frame.pack()
    Label(login_frame, text="Admin Login").grid(row=0, columnspan=2)
    Label(login_frame, text="Username:").grid(row=1, column=0)
    username_entry = Entry(login_frame)
    username_entry.grid(row=1, column=1)
    Label(login_frame, text="Password:").grid(row=2, column=0)
    password_entry = Entry(login_frame, show="*")
    password_entry.grid(row=2, column=1)
    login_button = Button(login_frame, text="Login", command=login_click)
    login_button.grid(row=3, columnspan=2)
    Label(login_frame, text="Or").grid(row=4, columnspan=2)
    customer_button = Button(root, text="Customer", command=display_buy_window)
    customer_button.pack()
    root.mainloop()
create_tables()
menu()