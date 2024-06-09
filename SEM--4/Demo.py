import sqlite3
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect('passport_system.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS record (
                name TEXT,
                email TEXT,
                phone TEXT,
                birth TEXT,
                aadhar TEXT
            )''')

def create_record(name, email, phone, birth, aadhar):
    c.execute("INSERT INTO record VALUES (?, ?, ?, ?, ?)", (name, email, phone, birth, aadhar))
    conn.commit()

def create():
    def add():
        create_record(entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(), entry_5.get())
        top.destroy()
        messagebox.showinfo("Success Message","Your Passport will be approve within 24hrs")
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
SIGN_IN = Button(root, text="SIGN IN", command=create)
SIGN_IN.place(x=120, y=150)
root.mainloop()
conn.close()
