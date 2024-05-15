import sqlite3
from tkinter import *

# Establishing connection and creating cursor
conn = sqlite3.connect('passport_system.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS record (
                name TEXT,
                email TEXT,
                phone TEXT,
                birth TEXT,
                aadhar TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS approved (
                name TEXT,
                email TEXT,
                phone TEXT,
                birth TEXT,
                aadhar TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT
            )''')

# Functions for database operations
def create_record(name, email, phone, birth, aadhar):
    c.execute("INSERT INTO record VALUES (?, ?, ?, ?, ?)", (name, email, phone, birth, aadhar))
    conn.commit()

def approve_all_records():
    c.execute("SELECT * FROM record")
    records_not_approved = c.fetchall()
    c.executemany("INSERT INTO approved VALUES (?, ?, ?, ?, ?)", records_not_approved)
    conn.commit()

def check_credentials(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

def record_check():
    c.execute("SELECT * FROM record")
    records_data = c.fetchall()
    c.execute("SELECT * FROM approved")
    approved_data = set(c.fetchall())
    difference = [record for record in records_data if tuple(record) not in approved_data]
    return difference

def track(name, phone):
    c.execute("SELECT * FROM record WHERE name=? AND phone=?", (name, phone))
    found = c.fetchone()
    if found:
        c.execute("SELECT * FROM approved WHERE name=? AND phone=?", (name, phone))
        approved_found = c.fetchone()
        if approved_found:
            track_1(True)
            return
        track_1(False)
    else:
        track_1(None)

def track_1(found):
    track_window = Tk()
    track_window.geometry('200x80')
    track_window.title("Passport Verification Status")
    if found == True:
        status_label = Label(track_window, text="")
        status_label_1 = Label(track_window, text="Your Passport")
        status_label_2 = Label(track_window, text="Verification Successful")
    elif found == False:
        status_label = Label(track_window, text="")
        status_label_1 = Label(track_window, text="Your Passport")
        status_label_2 = Label(track_window, text="Verification is still pending")
    else:
        status_label = Label(track_window, text="")
        status_label_1 = Label(track_window, text="Incorrect Detail")
        status_label_2 = Label(track_window, text="Check your details")
    status_label.pack()
    status_label_1.pack()
    status_label_2.pack()
    track_window.mainloop()

def login():
    username = e1.get()
    password = e2.get()
    if username == 'admin' and password == 'admin':
        root.destroy()
        admin_window()
    elif check_credentials(username, password):
        root.destroy()
        menu()

def admin_window():
    def approve_all_records():
        c.execute("SELECT * FROM record")
        records_not_approved = c.fetchall()
        c.executemany("INSERT INTO approved VALUES (?, ?, ?, ?, ?)", records_not_approved)
        conn.commit()
        admin_root.destroy()
    admin_root = Tk()
    admin_root.geometry('500x300')
    admin_root.title("Admin Panel")
    records_not_approved = record_check()
    records_label = Label(admin_root, text="Records not approved:")
    records_label.pack()
    records_text = Text(admin_root, height=10, width=60)
    for record in records_not_approved:
        records_text.insert(END, ', '.join(record) + '\n')
    records_text.pack()
    approve_button = Button(admin_root, text="Approve All", command=approve_all_records)
    approve_button.pack(pady=10)
    admin_root.mainloop()

def create_user(username, password):
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()

def create():
    def add():
        create_record(entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(), entry_5.get())
        top.destroy()
    top = Tk()
    top.geometry("300x350")
    top.title("Adding New Passport")
    Name = Label(top, text="Name")
    Name.place(x=30, y=50)
    EMail = Label(top, text="E-Mail")
    EMail.place(x=30, y=90)
    Phone = Label(top, text="Phone")
    Phone.place(x=30, y=130)
    Birth_Cer = Label(top, text="Date of Birth")
    Birth_Cer.place(x=30, y=170)
    Aadhar = Label(top, text="Aadhar")
    Aadhar.place(x=30, y=210)
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
    add = Button(top, text="ADD", command=add)
    add.place(x=70, y=280)
    close = Button(top, text="CLOSE", command=top.destroy)
    close.place(x=180, y=280)
    top.mainloop()

def track_page():
    root = Tk()
    root.geometry('300x200')
    root.title("Status Track")
    name = Label(root, text="Name")
    name.place(x=30, y=50)
    passwd = Label(root, text="Phone Number")
    passwd.place(x=30, y=90)
    e1 = Entry(root, width=20)
    e1.place(x=140, y=50)
    e2 = Entry(root, width=20)
    e2.place(x=140, y=90)
    SIGN_IN = Button(root, text="TRACK", command=lambda: track(e1.get(), e2.get()))
    SIGN_IN.place(x=120, y=150)
    root.mainloop()

def menu():
    def on_create():
        t_op.destroy()
        create()
    def op_destroy():
        t_op.destroy()
        again_login()
    t_op = Tk()
    t_op.geometry("250x180")
    t_op.title("Adding New Passport")
    exit_button = Button(t_op, text="Sign Out", command=op_destroy)
    exit_button.place(x=193, y=0)
    new_button = Button(t_op, text="New Passport", command=on_create)
    new_button.place(x=85, y=60)
    Close = Button(t_op, text="Track", command=track_page)
    Close.place(x=105, y=110)
    t_op.mainloop()

def NEW_USER():
    def on_create():
        create_user(entry_1.get(), entry_2.get())
        Root.destroy()
    Root = Tk()
    Root.geometry('300x200')
    Root.title("NEW USER")
    Name = Label(Root, text="User Name")
    Name.place(x=30, y=50)
    Passwd = Label(Root, text="Password")
    Passwd.place(x=30, y=90)
    entry_1 = Entry(Root, width=20)
    entry_1.place(x=140, y=50)
    entry_2 = Entry(Root, width=20)
    entry_2.place(x=140, y=90)
    Create = Button(Root, text="Create", command=on_create)
    Create.place(x=120, y=150)
    Root.mainloop()

def again_login():
    root = Tk()
    root.geometry('300x200')
    root.title("Passport System")
    Name = Label(root, text="Name")
    Name.place(x=30, y=50)
    Passwd = Label(root, text="Password")
    Passwd.place(x=30, y=90)
    e1 = Entry(root, width=20)
    e1.place(x=140, y=50)
    e2 = Entry(root, width=20, show="*")
    e2.place(x=140, y=90)
    SIGN_IN = Button(root, text="SIGN IN", command=login)
    SIGN_IN.place(x=120, y=150)
    root.mainloop()

root = Tk()
root.geometry('300x200')
root.title("Passport System")
Name = Label(root, text="Name")
Name.place(x=30, y=50)
Passwd = Label(root, text="Password")
Passwd.place(x=30, y=90)
e1 = Entry(root, width=20)
e1.place(x=140, y=50)
e2 = Entry(root, width=20, show="*")
e2.place(x=140, y=90)
SIGN_IN = Button(root, text="SIGN IN", command=login)
SIGN_IN.place(x=60, y=150)
SIGN_UP = Button(root, text="SIGN UP", command=NEW_USER)
SIGN_UP.place(x=190, y=150)
root.mainloop()

# Don't forget to close the connection when the program ends
conn.close()