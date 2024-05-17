import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Database Initialization
conn = sqlite3.connect('bpo_management.db')
c = conn.cursor()

# Create tables if not exists
c.execute('''CREATE TABLE IF NOT EXISTS employees (
             id INTEGER PRIMARY KEY,
             username TEXT UNIQUE,
             password TEXT,
             designation TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS agreements (
             id INTEGER PRIMARY KEY,
             company_name TEXT,
             product_name TEXT,
             quantity INTEGER,
             date TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS payments (
             id INTEGER PRIMARY KEY,
             company_name TEXT,
             product_name TEXT,
             amount REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (
             id INTEGER PRIMARY KEY,
             product_name TEXT,
             quantity INTEGER)''')

# GUI Class
class BPOManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("BPO Management System")

        # Login Frame
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)

        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.create_employee_button = tk.Button(self.login_frame, text="Create New Employee", command=self.create_employee_window)
        self.create_employee_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=5)

    def create_employee_window(self):
        employee_window = tk.Toplevel(self.master)
        employee_window.title("Create New Employee")

        tk.Label(employee_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry_new = tk.Entry(employee_window)
        self.username_entry_new.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(employee_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry_new = tk.Entry(employee_window, show="*")
        self.password_entry_new.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(employee_window, text="Designation:").grid(row=2, column=0, padx=10, pady=5)
        self.designation_entry_new = tk.Entry(employee_window)
        self.designation_entry_new.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(employee_window, text="Create", command=self.create_employee).grid(row=3, column=0, columnspan=2, pady=5)

    def create_employee(self):
        username = self.username_entry_new.get()
        password = self.password_entry_new.get()
        designation = self.designation_entry_new.get()
        if username and password and designation:
            try:
                c.execute("INSERT INTO employees (username, password, designation) VALUES (?, ?, ?)", (username, password, designation))
                conn.commit()
                messagebox.showinfo("Success", "Employee created successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        c.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
        employee = c.fetchone()
        if employee:
            if username == 'admin' and password == 'admin':
                self.show_admin_page()
            else:
                self.show_employee_page()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def show_admin_page(self):
        self.master.withdraw()  # Hide login window
        admin_page = tk.Toplevel()
        admin_page.title("Admin Page")

        # Admin page UI
        employee_details_button = tk.Button(admin_page, text="View Employee Details", command=self.view_employee_details)
        employee_details_button.pack()

        agreements_details_button = tk.Button(admin_page, text="View Agreements Details", command=self.view_agreements_details)
        agreements_details_button.pack()

        payments_details_button = tk.Button(admin_page, text="View Payments Details", command=self.view_payments_details)
        payments_details_button.pack()
        
        other_company_products_button = tk.Button(admin_page, text="View Other Company Products", command=self.view_other_company_products)
        other_company_products_button.pack()

        product_exchange_button = tk.Button(admin_page, text="Product Exchange", command=self.product_exchange)
        product_exchange_button.pack()

    def show_employee_page(self):
        self.master.withdraw()  # Hide login window
        employee_page = tk.Toplevel()
        employee_page.title("Employee Page")

        # Employee page UI
        self.create_agreement_button = tk.Button(employee_page, text="Create Agreement", command=self.create_agreement_window)
        self.create_agreement_button.pack(pady=5)

        self.make_payment_button = tk.Button(employee_page, text="Make Payment", command=self.make_payment_window)
        self.make_payment_button.pack(pady=5)

        self.complaint_feedback_button = tk.Button(employee_page, text="Complaint/Feedback", command=self.complaint_feedback_window)
        self.complaint_feedback_button.pack(pady=5)

    def create_agreement_window(self):
        agreement_window = tk.Toplevel(self.master)
        agreement_window.title("Create Agreement")

        tk.Label(agreement_window, text="Company Name:").grid(row=0, column=0, padx=10, pady=5)
        self.company_name_entry = tk.Entry(agreement_window)
        self.company_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(agreement_window, text="Product Name:").grid(row=1, column=0, padx=10, pady=5)
        self.product_name_entry = tk.Entry(agreement_window)
        self.product_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(agreement_window, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
        self.quantity_entry = tk.Entry(agreement_window)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(agreement_window, text="Date:").grid(row=3, column=0, padx=10, pady=5)
        self.date_entry = tk.Entry(agreement_window)
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(agreement_window, text="Create", command=self.create_agreement).grid(row=4, column=0, columnspan=2, pady=5)

    def create_agreement(self):
        company_name = self.company_name_entry.get()
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        date = self.date_entry.get()
        if company_name and product_name and quantity and date:
            try:
                c.execute("INSERT INTO agreements (company_name, product_name, quantity, date) VALUES (?, ?, ?, ?)", (company_name, product_name, quantity, date))
                conn.commit()
                messagebox.showinfo("Agreement Sent", "Agreement sent to other company!")
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "ERROR")

    def make_payment_window(self):
        payment_window = tk.Toplevel(self.master)
        payment_window.title("Make Payment")

        tk.Label(payment_window, text="Company Name:").grid(row=0, column=0, padx=10, pady=5)
        self.company_name_payment_entry = tk.Entry(payment_window)
        self.company_name_payment_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(payment_window, text="Product Name:").grid(row=1, column=0, padx=10, pady=5)
        self.product_name_payment_entry = tk.Entry(payment_window)
        self.product_name_payment_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(payment_window, text="Amount:").grid(row=2, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(payment_window)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(payment_window, text="Make Payment", command=self.make_payment).grid(row=3, column=0, columnspan=2, pady=5)

    def make_payment(self):
        company_name = self.company_name_payment_entry.get()
        product_name = self.product_name_payment_entry.get()
        amount = self.amount_entry.get()
        if company_name and product_name and amount:
             try:
                c.execute("INSERT INTO payments (company_name, product_name, amount) VALUES (?, ?, ?)", (company_name, product_name, amount))
                conn.commit()
                messagebox.showinfo("Payment Transfer", "Payment transfer is successful!")
             
             except sqlite3.IntegrityError:
                messagebox.showerror("Error", "ERROR")

    def complaint_feedback_window(self):
        complaint_feedback_window = tk.Toplevel(self.master)
        complaint_feedback_window.title("Complaint/Feedback")

        tk.Label(complaint_feedback_window, text="Company Name:").grid(row=0, column=0, padx=10, pady=5)
        self.company_name_complaint_entry = tk.Entry(complaint_feedback_window)
        self.company_name_complaint_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(complaint_feedback_window, text="Product Name:").grid(row=1, column=0, padx=10, pady=5)
        self.product_name_complaint_entry = tk.Entry(complaint_feedback_window)
        self.product_name_complaint_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(complaint_feedback_window, text="Complaint/Feedback:").grid(row=2, column=0, padx=10, pady=5)
        self.complaint_feedback_entry = tk.Entry(complaint_feedback_window)
        self.complaint_feedback_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(complaint_feedback_window, text="Submit", command=self.complaint_feedback).grid(row=3, column=0, columnspan=2, pady=5)

    def complaint_feedback(self):
        company_name = self.company_name_complaint_entry.get()
        product_name = self.product_name_complaint_entry.get()
        complaint_feedback = self.complaint_feedback_entry.get()
        if company_name and product_name and complaint_feedback:
            # Assuming here that you have a way to submit the complaint/feedback, so just displaying a message box
            messagebox.showinfo("Complaint/Feedback", "Complaint/Feedback submitted successfully!")

    def view_employee_details(self):
        # Fetch data from the employees table
        c.execute("SELECT * FROM employees")
        employees = c.fetchall()

        # Create a new window to display employee details
        employee_details_window = tk.Toplevel(self.master)
        employee_details_window.title("Employee Details")

        # Create a frame to hold the employee details
        employee_frame = tk.Frame(employee_details_window)
        employee_frame.pack(padx=20, pady=20)

        # Header labels
        headers = ["ID", "Username", "Password", "Designation"]
        for col, header in enumerate(headers):
            tk.Label(employee_frame, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)

        # Display employee details
        for row_num, employee in enumerate(employees, start=1):
            for col, value in enumerate(employee):
                tk.Label(employee_frame, text=value).grid(row=row_num, column=col, padx=5, pady=5)

    def view_agreements_details(self):
        # Fetch data from the agreements table
        c.execute("SELECT * FROM agreements")
        agreements = c.fetchall()

        # Create a new window to display agreement details
        agreement_details_window = tk.Toplevel(self.master)
        agreement_details_window.title("Agreement Details")

        # Create a frame to hold the agreement details
        agreement_frame = tk.Frame(agreement_details_window)
        agreement_frame.pack(padx=20, pady=20)

        # Header labels
        headers = ["ID", "Company Name", "Product Name", "Quantity", "Date"]
        for col, header in enumerate(headers):
            tk.Label(agreement_frame, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)

        # Display agreement details
        for row_num, agreement in enumerate(agreements, start=1):
            for col, value in enumerate(agreement):
                tk.Label(agreement_frame, text=value).grid(row=row_num, column=col, padx=5, pady=5)

    def view_payments_details(self):
        # Fetch data from the payments table
        c.execute("SELECT * FROM payments")
        payments = c.fetchall()

        # Create a new window to display payment details
        payment_details_window = tk.Toplevel(self.master)
        payment_details_window.title("Payment Details")

        # Create a frame to hold the payment details
        payment_frame = tk.Frame(payment_details_window)
        payment_frame.pack(padx=20, pady=20)

        # Header labels
        headers = ["ID", "Company Name", "Product Name", "Amount"]
        for col, header in enumerate(headers):
            tk.Label(payment_frame, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)

        # Display payment details
        for row_num, payment in enumerate(payments, start=1):
            for col, value in enumerate(payment):
                tk.Label(payment_frame, text=value).grid(row=row_num, column=col, padx=5, pady=5)
    def view_other_company_products(self):
        # Fetch data from the products table
        c.execute("SELECT * FROM products")
        products = c.fetchall()

        # Create a new window to display product details
        product_details_window = tk.Toplevel(self.master)
        product_details_window.title("Other Company Products")

        # Create a frame to hold the product details
        product_frame = tk.Frame(product_details_window)
        product_frame.pack(padx=20, pady=20)

        # Header labels
        headers = ["ID", "Product Name", "Quantity"]
        for col, header in enumerate(headers):
            tk.Label(product_frame, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)

        # Display product details
        for row_num, product in enumerate(products, start=1):
            for col, value in enumerate(product):
                tk.Label(product_frame, text=value).grid(row=row_num, column=col, padx=5, pady=5)

    def product_exchange(self):
        # Implement the functionality for product exchange here
        pass

    def view_products(self):
        # Fetch data from the products table
        c.execute("SELECT * FROM products")
        products = c.fetchall()

        # Create a new window to display product details
        product_details_window = tk.Toplevel(self.master)
        product_details_window.title("Products")

        # Create a frame to hold the product details
        product_frame = tk.Frame(product_details_window)
        product_frame.pack(padx=20, pady=20)

        # Header labels
        headers = ["ID", "Product Name", "Quantity"]
        for col, header in enumerate(headers):
            tk.Label(product_frame, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)

        # Display product details
        for row_num, product in enumerate(products, start=1):
            for col, value in enumerate(product):
                tk.Label(product_frame, text=value).grid(row=row_num, column=col, padx=5, pady=5)



def main():
    root = tk.Tk()
    app = BPOManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()

conn.close()
