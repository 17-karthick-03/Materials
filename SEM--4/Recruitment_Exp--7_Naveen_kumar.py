import sqlite3
from tkinter import *
from tkinter import messagebox

# Establishing connection and creating cursor
conn = sqlite3.connect('recruitment_system.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS applicants (
                name TEXT,
                gender TEXT,
                qualification TEXT,
                experience TEXT,
                email TEXT PRIMARY KEY,
                phone TEXT,
                address TEXT,
                status TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )''')

# Functions for database operations
def submit_details(name, gender, qualification, experience, email, phone, address):
    try:
        c.execute("INSERT INTO applicants VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, gender, qualification, experience, email, phone, address, "Pending"))
        conn.commit()
        messagebox.showinfo("Success", "Details are submitted successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "An applicant with this email already exists.")

def track_status():
    def track():
        c.execute("SELECT * FROM applicants WHERE email=?", (email_entry.get(),))
        applicant_data = c.fetchone()
        if applicant_data:
            status_label.config(text=f"Application Status: {applicant_data[-1]}")
        else:
            status_label.config(text="No application found with this email.")
            
    track_window = Toplevel()
    track_window.geometry('300x200')
    track_window.title("Track Application Status")
    
    email_label = Label(track_window, text="Enter Email:")
    email_label.pack()
    email_entry = Entry(track_window, width=30)
    email_entry.pack()
    
    track_button = Button(track_window, text="Track", command=track)
    track_button.pack(pady=10)
    
    status_label = Label(track_window, text="")
    status_label.pack()

def hr_page():
    def update_status(status, email):
        c.execute("UPDATE applicants SET status=? WHERE email=?", (status, email))
        conn.commit()
        hr_window.destroy()
        hr_page()
        
    hr_window = Toplevel()
    hr_window.geometry('800x600')
    hr_window.title("HR Panel")
    
    applicants_label = Label(hr_window, text="Applicants Details:")
    applicants_label.grid(row=0, column=0, columnspan=3)
    
    c.execute("SELECT * FROM applicants WHERE status='Pending'")
    all_applicants = c.fetchall()
    
    for i, applicant in enumerate(all_applicants):
        applicant_details = f"{applicant[0]}, {applicant[1]}, {applicant[2]}, {applicant[3]}, {applicant[4]}, {applicant[5]}, {applicant[6]}"
        applicant_label = Label(hr_window, text=applicant_details)
        applicant_label.grid(row=i+1, column=0, sticky='w')
        
        accept_button = Button(hr_window, text="Accept", command=lambda email=applicant[4]: update_status("Accepted", email))
        accept_button.grid(row=i+1, column=1)
        
        reject_button = Button(hr_window, text="Reject", command=lambda email=applicant[4]: update_status("Rejected", email))
        reject_button.grid(row=i+1, column=2)

def applicant_page():
    def submit():
        submit_details(name_entry.get(), gender_entry.get(), qualification_entry.get(), experience_entry.get(),
                       email_entry.get(), phone_entry.get(), address_entry.get())
        
    applicant_window = Toplevel()
    applicant_window.geometry('400x400')
    applicant_window.title("Applicant Panel")
    
    name_label = Label(applicant_window, text="Name:")
    name_label.pack()
    name_entry = Entry(applicant_window, width=30)
    name_entry.pack()
    
    gender_label = Label(applicant_window, text="Gender:")
    gender_label.pack()
    gender_entry = Entry(applicant_window, width=30)
    gender_entry.pack()
    
    qualification_label = Label(applicant_window, text="Qualification:")
    qualification_label.pack()
    qualification_entry = Entry(applicant_window, width=30)
    qualification_entry.pack()
    
    experience_label = Label(applicant_window, text="Experience:")
    experience_label.pack()
    experience_entry = Entry(applicant_window, width=30)
    experience_entry.pack()
    
    email_label = Label(applicant_window, text="Email:")
    email_label.pack()
    email_entry = Entry(applicant_window, width=30)
    email_entry.pack()
    
    phone_label = Label(applicant_window, text="Phone:")
    phone_label.pack()
    phone_entry = Entry(applicant_window, width=30)
    phone_entry.pack()
    
    address_label = Label(applicant_window, text="Address:")
    address_label.pack()
    address_entry = Entry(applicant_window, width=30)
    address_entry.pack()
    
    submit_button = Button(applicant_window, text="Submit", command=submit)
    submit_button.pack(pady=10)
    
    track_button = Button(applicant_window, text="Track Application Status", command=track_status)
    track_button.pack(pady=10)

def signup():
    def create_user():
        username = username_entry.get()
        password = password_entry.get()
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "User created successfully. You can now log in.")
        signup_window.destroy()
    
    signup_window = Toplevel()
    signup_window.geometry('300x200')
    signup_window.title("Sign Up")
    
    username_label = Label(signup_window, text="Username:")
    username_label.pack()
    username_entry = Entry(signup_window, width=30)
    username_entry.pack()
    
    password_label = Label(signup_window, text="Password:")
    password_label.pack()
    password_entry = Entry(signup_window, width=30, show="*")
    password_entry.pack()
    
    signup_button = Button(signup_window, text="Sign Up", command=create_user)
    signup_button.pack(pady=10)

# Main login window
root = Tk()
root.geometry('300x200')
root.title("Recruitment System")

def login():
    username = e1.get()
    password = e2.get()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        root.withdraw()
        if username == 'admin':
            hr_page()
        else:
            applicant_page()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

Name = Label(root, text="Username")
Name.place(x=30, y=50)
Passwd = Label(root, text="Password")
Passwd.place(x=30, y=90)
e1 = Entry(root, width=20)
e1.place(x=140, y=50)
e2 = Entry(root, width=20, show="*")
e2.place(x=140, y=90)
SIGN_IN = Button(root, text="SIGN IN", command=login)
SIGN_IN.place(x=60, y=150)

SIGN_UP = Button(root, text="SIGN UP", command=signup)
SIGN_UP.place(x=190, y=150)

root.mainloop()

# Don't forget to close the connection when the program ends
conn.close()
