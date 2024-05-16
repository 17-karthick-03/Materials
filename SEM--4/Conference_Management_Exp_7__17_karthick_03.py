import sqlite3
from tkinter import *
conn = sqlite3.connect('conference_system.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                status TEXT DEFAULT 'Pending'
            )''')
c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT
            )''')
def submit_paper(title, author):
    c.execute("INSERT INTO papers (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
def approve_paper(paper_id):
    c.execute("UPDATE papers SET status='Approved' WHERE id=?", (paper_id,))
    conn.commit()
def track_paper(author):
    c.execute("SELECT * FROM papers WHERE author=?", (author,))
    return c.fetchall()
def check_credentials(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None
def create_user(username, password):
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
def login():
    username = e1.get()
    password = e2.get()
    if username == 'admin' and password == 'admin':
        root.destroy()
        admin_window()
    elif check_credentials(username, password):
        root.destroy()
        menu()
    else:
        print("Invalid username or password")
def submit_paper_page():
    def add_paper():
        submit_paper(entry_1.get(), entry_2.get())
        top.destroy()
    top = Tk()
    top.geometry("300x250")
    top.title("Submit New Paper")
    Title = Label(top, text="Paper Title")
    Title.place(x=30, y=50)
    Author = Label(top, text="Author")
    Author.place(x=30, y=90)
    entry_1 = Entry(top, width=20)
    entry_1.place(x=140, y=50)
    entry_2 = Entry(top, width=20)
    entry_2.place(x=140, y=90)
    submit = Button(top, text="SUBMIT", command=add_paper)
    submit.place(x=70, y=160)
    close = Button(top, text="CLOSE", command=top.destroy)
    close.place(x=180, y=160)
    top.mainloop()
def track_page():
    def track():
        papers = track_paper(entry_1.get())
        top.destroy()
        track_result(papers)
    top = Tk()
    top.geometry("300x150")
    top.title("Track Paper")
    Author = Label(top, text="Author")
    Author.place(x=30, y=50)
    entry_1 = Entry(top, width=20)
    entry_1.place(x=140, y=50)
    track = Button(top, text="TRACK", command=track)
    track.place(x=120, y=100)
    top.mainloop()
def track_result(papers):
    result_window = Tk()
    result_window.geometry('400x300')
    result_window.title("Paper Submission Status")
    result_label = Label(result_window, text="Your Paper Submission Status:")
    result_label.pack()
    papers_text = Text(result_window, height=10, width=60)
    for paper in papers:
        papers_text.insert(END, f'Title: {paper[1]}, Status: {paper[3]}\n')
    papers_text.pack()
    result_window.mainloop()
def admin_window():
    def approve_all_papers():
        c.execute("UPDATE papers SET status='Approved' WHERE status='Pending'")
        conn.commit()
        admin_root.destroy()
    admin_root = Tk()
    admin_root.geometry('500x300')
    admin_root.title("Admin Panel")
    papers_pending = c.execute("SELECT * FROM papers WHERE status='Pending'").fetchall()
    records_label = Label(admin_root, text="Papers Pending Approval:")
    records_label.pack()
    records_text = Text(admin_root, height=10, width=60)
    for paper in papers_pending:
        records_text.insert(END, f'ID: {paper[0]}, Title: {paper[1]}, Author: {paper[2]}\n')
    records_text.pack()
    approve_button = Button(admin_root, text="Approve All", command=approve_all_papers)
    approve_button.pack(pady=10)
    admin_root.mainloop()
def menu():
    def on_submit():
        t_op.destroy()
        submit_paper_page()
    def op_destroy():
        t_op.destroy()
        again_login()
    t_op = Tk()
    t_op.geometry("250x180")
    t_op.title("Conference Management System")
    exit_button = Button(t_op, text="Sign Out", command=op_destroy)
    exit_button.place(x=193, y=0)
    new_button = Button(t_op, text="Submit Paper", command=on_submit)
    new_button.place(x=85, y=60)
    track_button = Button(t_op, text="Track Paper", command=track_page)
    track_button.place(x=85, y=110)
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
    root.title("Conference Management System")
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
root.title("Conference Management System")
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
conn.close()
