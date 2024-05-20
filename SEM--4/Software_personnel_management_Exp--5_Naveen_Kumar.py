import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            name TEXT PRIMARY KEY,
            emp_id TEXT,
            designation TEXT,
            performance TEXT,
            salary REAL,
            dearness_allowance REAL,
            house_allowance REAL,
            medical_allowance REAL
        )
    ''')
    conn.commit()
    conn.close()

# Main application
class ManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Management System")
        self.geometry("400x400")
        init_db()
        self.show_login()

    def show_login(self):
        self.clear_frame()
        tk.Label(self, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        
        tk.Label(self, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "admin":
            self.show_manager_page()
        else:
            conn = sqlite3.connect('employees.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE name = ? AND emp_id = ?", (username, password))
            employee = cursor.fetchone()
            conn.close()
            
            if employee:
                self.show_employee_details(employee)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

    def show_manager_page(self):
        self.clear_frame()
        tk.Label(self, text="Manager Page").pack(pady=10)
        
        self.emp_name = self.create_entry("Employee Name")
        self.emp_id = self.create_entry("Employee ID")
        self.emp_designation = self.create_entry("Designation")
        self.emp_performance = self.create_entry("Performance")
        self.emp_salary = self.create_entry("Salary")
        self.emp_da = self.create_entry("Dearness Allowance")
        self.emp_ha = self.create_entry("House Allowance")
        self.emp_ma = self.create_entry("Medical Allowance")
        
        tk.Button(self, text="Submit", command=self.save_employee).pack(pady=20)
        
    def create_entry(self, label):
        tk.Label(self, text=label).pack(pady=2)
        entry = tk.Entry(self)
        entry.pack(pady=2)
        return entry
    
    def save_employee(self):
        emp_name = self.emp_name.get()
        emp_id = self.emp_id.get()
        designation = self.emp_designation.get()
        performance = self.emp_performance.get()
        salary = float(self.emp_salary.get())
        da = float(self.emp_da.get())
        ha = float(self.emp_ha.get())
        ma = float(self.emp_ma.get())
        
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO employees 
            (name, emp_id, designation, performance, salary, dearness_allowance, house_allowance, medical_allowance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (emp_name, emp_id, designation, performance, salary, da, ha, ma))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Details of {emp_name} saved successfully")

    def show_employee_details(self, employee):
        self.clear_frame()
        tk.Label(self, text=f"Details for {employee[0]}").pack(pady=10)
        
        details = [
            ("Name", employee[0]),
            ("Employee ID", employee[1]),
            ("Designation", employee[2]),
            ("Performance", employee[3]),
            ("Salary", employee[4]),
            ("Dearness Allowance", employee[5]),
            ("House Allowance", employee[6]),
            ("Medical Allowance", employee[7])
        ]
        
        for label, value in details:
            tk.Label(self, text=f"{label}: {value}").pack(pady=2)
        
        tk.Button(self, text="Logout", command=self.show_login).pack(pady=20)
    
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

# Running the application
if __name__ == "__main__":
    app = ManagementApp()
    app.mainloop()
