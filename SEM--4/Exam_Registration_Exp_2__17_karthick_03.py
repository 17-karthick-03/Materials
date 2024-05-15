import sqlite3
from tkinter import *
def create_tables():
    conn = sqlite3.connect('exam.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS course (
                        reg_num TEXT,
                        dob TEXT,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        total_amount REAL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                        name TEXT,
                        dob TEXT,
                        reg_num TEXT,
                        phone TEXT,
                        email TEXT,
                        aadhar TEXT,
                        course TEXT,
                        department TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                        reg_num TEXT,
                        dob TEXT
                    )''')
    conn.commit()
    conn.close()
def check_course_registration(reg_num, dob):
    conn = sqlite3.connect('exam.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE reg_num = ? AND dob = ?", (reg_num, dob))
    row = cursor.fetchone()
    conn.close()
    return row
def process_payment(reg_num, dob, upi_id):
    course_data = check_course_registration(reg_num, dob)
    if course_data:
        total_amount = 165000
        name = course_data[0]
        success_message_1 = f"Hello {name},"
        success_message_2 = f"Your payment of ₹ {total_amount} was successful."
        success_message_3 = "Online generated receipt will be mailed to you on registered email id."
        display_payment_success_message(success_message_1, success_message_2, success_message_3)
def display_payment_success_message(msg_1, msg_2, msg_3):
    success_window = Tk()
    success_window.geometry('500x100')
    success_window.title("Payment Status")
    Label(success_window, text=msg_1).pack()
    Label(success_window, text=msg_2).pack()
    Label(success_window, text=msg_3).pack()
    success_window.mainloop()
def display_payment_error_message(message):
    error_window = Tk()
    error_window.geometry('300x100')
    error_window.title("Payment Error")
    Label(error_window, text=message).pack(pady=20)
    error_window.mainloop()
def open_payment_window():
    def process_payment_click():
        reg_num = reg_entry.get()
        dob = dob_entry.get()
        if reg_num and dob:
            if check_course_registration(reg_num, dob):
                payment_page(reg_num, dob)
            else:
                display_payment_error_message("Wrong Credentials")
    payment_window = Tk()
    payment_window.geometry("300x200")
    payment_window.title("Payment")
    Label(payment_window, text="Reg Num").place(x=30, y=50)
    Label(payment_window, text="Date of Birth").place(x=30, y=85)
    Label(payment_window, text="Ex : 19022005").place(x=30, y=100)
    reg_entry = Entry(payment_window, width=20)
    reg_entry.place(x=140, y=50)
    dob_entry = Entry(payment_window, width=20, show="*")
    dob_entry.place(x=140, y=90)
    Button(payment_window, text="Proceed to Payment", command=process_payment_click).place(x=80, y=150)
    payment_window.mainloop()
def payment_page(reg_num, dob):
    def process_payment_click():
        upi_id = upi_entry.get()
        if upi_id:
            process_payment(reg_num, dob, upi_id)
    course_data = check_course_registration(reg_num, dob)
    payment_page_window = Tk()
    payment_page_window.geometry("300x200")
    payment_page_window.title("Payment Page")
    Label(payment_page_window, text=f"Total Amount: ₹ 165000").pack()
    Label(payment_page_window, text="Enter UPI ID:").pack()
    upi_entry = Entry(payment_page_window, width=30)
    upi_entry.pack()
    Button(payment_page_window, text="Pay", command=process_payment_click).pack(pady=10)
    payment_page_window.mainloop()
def create_record(name, dob, reg_num, phone, email, aadhar, course, department):
    conn = sqlite3.connect('exam.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (name, dob, reg_num, phone, email, aadhar, course, department))
    conn.commit()
    conn.close()
def create():
    def add():
        create_record(entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(), entry_5.get(), entry_6.get(), course_var.get(), department_var.get())
        top.destroy()
    top = Tk()
    top.geometry("400x450")
    top.title("Exam Registration Form")
    name_label = Label(top, text="Full Name:")
    name_label.place(x=30, y=50)
    dob_label = Label(top, text="DOB (DDMMYYYY):")
    dob_label.place(x=30, y=90)
    reg_label = Label(top, text="Register No.:")
    reg_label.place(x=30, y=130)
    phone_label = Label(top, text="Phone Number:")
    phone_label.place(x=30, y=170)
    email_label = Label(top, text="Email Address:")
    email_label.place(x=30, y=210)
    aadhar_label = Label(top, text="Aadhar Number:")
    aadhar_label.place(x=30, y=250)
    entry_1 = Entry(top, width=20)
    entry_1.place(x=140, y=50)
    entry_2 = Entry(top, width=20)
    entry_2.place(x=140, y=90)
    entry_3 = Entry(top, width=20)
    entry_3.place(x=140, y=130)
    entry_4 = Entry(top, width=20)
    entry_4.place(x=140, y=170)
    entry_5 = Entry(top, width=20)
    entry_5.place(x=140, y=210)
    entry_6 = Entry(top, width=20)
    entry_6.place(x=140, y=250)
    Label(top, text="Select Course").place(x=160, y=290)
    course_var = StringVar()
    course_var.set("B.E.")  # Default value
    courses = ["B.E.", "B.Tech"]
    for i, course in enumerate(courses):
        Radiobutton(top, text=course, variable=course_var, value=course, anchor=W).place(x=140 + i * 60, y=320)
    Label(top, text="Select Department").place(x=150, y=350)
    department_var = StringVar()
    department_var.set("CSE")  # Default value
    departments = ["CSE", "ECE", "EIE", "EEE", "AIDS"]
    for i, department in enumerate(departments):
        Radiobutton(top, text=department, variable=department_var, value=department).place(x=50 + i * 60, y=380)
    add_button = Button(top, text="ADD", command=add)
    add_button.place(x=180, y=410)
    top.mainloop()
def menu():
    def op_destroy():
        t_op.destroy()
        again_login(root)
    t_op = Tk()
    t_op.geometry("250x180")
    t_op.title("Exam Registration")
    Button(t_op, text="Sign Out", command=op_destroy).place(x=193, y=0)
    Button(t_op, text="Apply", command=lambda: create()).place(x=105, y=60)
    Button(t_op, text="Payment", command=lambda: open_payment_window()).place(x=97, y=110)
    t_op.mainloop()
def again_login():
    def verify_login():
        reg_num = reg_entry.get()
        dob = dob_entry.get()
        conn = sqlite3.connect('exam.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE reg_num = ? AND dob = ?", (reg_num, dob))
        row = cursor.fetchone()
        conn.close()
        if row:
            login_window.destroy()
            menu()
        else:
            display_login_error_message("Incorrect credentials.")
    login_window = Tk()
    login_window.geometry('300x200')
    login_window.title("Exam Registration")
    Label(login_window, text="Reg Num").place(x=30, y=50)
    Label(login_window, text="Date of Birth").place(x=30, y=85)
    Label(login_window, text="Ex : 19022005").place(x=30, y=100)
    reg_entry = Entry(login_window, width=20)
    reg_entry.place(x=140, y=50)
    dob_entry = Entry(login_window, width=20, show="*")
    dob_entry.place(x=140, y=90)
    Button(login_window, text="SIGN IN", command=verify_login).place(x=120, y=150)
    login_window.mainloop()
def display_login_error_message(message):
    error_window = Tk()
    error_window.geometry('300x100')
    error_window.title("Login Error")
    Label(error_window, text=message).pack(pady=20)
    error_window.mainloop()
create_tables()
again_login()

"""import sqlite3

def create_login_table():
    conn = sqlite3.connect('exam.db')
    cursor = conn.cursor()

    # Create login table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                        reg_num TEXT,
                        dob TEXT
                    )''')

    # Insert data into login table
    login_data = [
        ("142222104073", "17032005"),
    ]

    cursor.executemany("INSERT INTO login VALUES (?, ?)", login_data)

    conn.commit()
    conn.close()

# Create login table and insert data
create_login_table()
"""
