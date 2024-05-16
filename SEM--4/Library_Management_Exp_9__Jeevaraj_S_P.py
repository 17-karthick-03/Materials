import sqlite3
from tkinter import *
from tkinter import messagebox
conn = sqlite3.connect('library.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS books (
                bid INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                status TEXT
                )''')
cur.execute('''CREATE TABLE IF NOT EXISTS books_issued (
                bid INTEGER PRIMARY KEY,
                issueto TEXT
                )''')
def issue_book():
    bid = inf1.get()
    issueto = inf2.get()
    try:
        cur.execute("SELECT status FROM books WHERE bid = ?", (bid,))
        check = cur.fetchone()
        if check and check[0] == 'avail':
            cur.execute("INSERT INTO books_issued (bid, issueto) VALUES (?, ?)", (bid, issueto))
            cur.execute("UPDATE books SET status = 'issued' WHERE bid = ?", (bid,))
            conn.commit()
            messagebox.showinfo('Success', "Book Issued Successfully")
        else:
            messagebox.showinfo('Message', "Book Already Issued or not available")
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to issue book: {e}")
def issue():
    global inf1, inf2
    issue_window = Tk()
    issue_window.title("Issue Book")
    issue_window.geometry("250x130")
    lb1 = Label(issue_window, text="Book ID : ")
    lb1.grid(row=0, column=0, padx=10, pady=5)
    inf1 = Entry(issue_window)
    inf1.grid(row=0, column=1, padx=10, pady=5)
    lb2 = Label(issue_window, text="Issued To : ")
    lb2.grid(row=1, column=0, padx=10, pady=5)
    inf2 = Entry(issue_window)
    inf2.grid(row=1, column=1, padx=10, pady=5)
    issueBtn = Button(issue_window, text="Issue", command=issue_book)
    issueBtn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    issue_window.mainloop()
def returnn():
    bid = bookInfo1.get()
    try:
        cur.execute("SELECT status FROM books WHERE bid = ?", (bid,))
        check = cur.fetchone()
        if check and check[0] == 'issued':
            cur.execute("DELETE FROM books_issued WHERE bid = ?", (bid,))
            cur.execute("UPDATE books SET status = 'avail' WHERE bid = ?", (bid,))
            conn.commit()
            messagebox.showinfo('Success', "Book Returned Successfully")
        else:
            messagebox.showinfo('Message', "Please check the book ID")
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to return book: {e}")
def returnBook():
    global bookInfo1
    return_window = Tk()
    return_window.title("Return Book")
    return_window.geometry("250x80")
    lb1 = Label(return_window, text="Book ID : ")
    lb1.grid(row=0, column=0, padx=10, pady=5)
    bookInfo1 = Entry(return_window)
    bookInfo1.grid(row=0, column=1, padx=15, pady=5)
    SubmitBtn = Button(return_window, text="Return", command=returnn)
    SubmitBtn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    return_window.mainloop()
def View():
    view_window = Tk()
    view_window.title("View Books")
    view_window.geometry("250x150")
    try:
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        for i, book in enumerate(books):
            for j, value in enumerate(book):
                Label(view_window, text=value).grid(row=i, column=j, padx=5, pady=3)
    except Exception as e:
        messagebox.showinfo("Failed to fetch files from database", f"Error: {e}")
    quitBtn = Button(view_window, text="Quit", command=view_window.destroy)
    quitBtn.grid(row=4, column=1, columnspan=4, padx=40, pady=10)
    view_window.mainloop()
def addBook():
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4
    add_window = Tk()
    add_window.title("Add Book")
    add_window.geometry("300x170")
    lb1 = Label(add_window, text="Book ID : ")
    lb1.grid(row=0, column=0, padx=10, pady=5)
    bookInfo1 = Entry(add_window)
    bookInfo1.grid(row=0, column=1, padx=10, pady=5)
    lb2 = Label(add_window, text="Title : ")
    lb2.grid(row=1, column=0, padx=10, pady=5)
    bookInfo2 = Entry(add_window)
    bookInfo2.grid(row=1, column=1, padx=10, pady=5)
    lb3 = Label(add_window, text="Author : ")
    lb3.grid(row=2, column=0, padx=10, pady=5)
    bookInfo3 = Entry(add_window)
    bookInfo3.grid(row=2, column=1, padx=10, pady=5)
    bookInfo4 = Entry(add_window)
    bookInfo4.insert(0, 'Avail')  # Default status to 'avail'
    lb4 = Label(add_window, text="Status(Avail/Issued) : ")
    lb4.grid(row=3, column=0, padx=10, pady=5)
    bookInfo4.grid(row=3, column=1, padx=10, pady=5)
    SubmitBtn = Button(add_window, text="SUBMIT", command=bookRegister)
    SubmitBtn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    add_window.mainloop()
def deleteBook():
    bid = bookInfo1.get()
    try:
        cur.execute("DELETE FROM books WHERE bid = ?", (bid,))
        conn.commit()
        messagebox.showinfo('Success', "Book Record Deleted Successfully")
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to delete book: {e}")
    bookInfo1.delete(0, END)
def delete():
    global bookInfo1
    delete_window = Tk()
    delete_window.title("Delete Book")
    delete_window.geometry("250x80")
    lb2 = Label(delete_window, text="Book ID : ")
    lb2.grid(row=0, column=0, padx=15, pady=5)
    bookInfo1 = Entry(delete_window)
    bookInfo1.grid(row=0, column=1, padx=10, pady=5)
    SubmitBtn = Button(delete_window, text="SUBMIT", command=deleteBook)
    SubmitBtn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    delete_window.mainloop()
def bookRegister():
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4
    bid = bookInfo1.get()
    title = bookInfo2.get()
    author = bookInfo3.get()
    status = bookInfo4.get()
    try:
        cur.execute("INSERT INTO books (bid, title, author, status) VALUES (?, ?, ?, ?)", (bid, title, author, status))
        conn.commit()
        messagebox.showinfo('Success', "Book added successfully")
    except Exception as e:
        messagebox.showinfo("Error", f"Can't add data into Database: {e}")
    bookInfo1.delete(0, END)
    bookInfo2.delete(0, END)
    bookInfo3.delete(0, END)
    bookInfo4.delete(0, END)
def main():
    root = Tk()
    root.geometry("300x250")
    root.title("Library Management System")
    btn1 = Button(root, text="Add Book", command=addBook)
    btn1.pack(pady=10)
    btn2 = Button(root, text="Delete Book", command=delete)
    btn2.pack(pady=10)
    btn3 = Button(root, text="Issue Book", command=issue)
    btn3.pack(pady=10)
    btn4 = Button(root, text="Return Book", command=returnBook)
    btn4.pack(pady=10)
    btn5 = Button(root, text="View Books", command=View)
    btn5.pack(pady=10)
    root.mainloop()
if __name__ == "__main__":
    main()
conn.close()
