import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect('course_reservation.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_details (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            name TEXT,
            age INTEGER,
            qualification TEXT,
            percentage REAL,
            email TEXT,
            payment_mode TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            course_name TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Insert admin user if not exists
    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    admin_exists = cursor.fetchone()
    if not admin_exists:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "pass", "admin"))

    conn.commit()
    conn.close()

# Main application
class CourseReservationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Course Reservation")
        self.geometry("400x300")
        init_db()
        self.create_widgets()

    def create_widgets(self):
        self.login_frame = LoginPage(self)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_user_page(self, user_id):
        self.login_frame.destroy()
        self.user_frame = UserPage(self, user_id)
        self.user_frame.pack(fill=tk.BOTH, expand=True)

    def show_admin_page(self):
        self.login_frame.destroy()
        self.admin_frame = AdminPage(self)
        self.admin_frame.pack(fill=tk.BOTH, expand=True)

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.signin_button = tk.Button(self, text="Sign In", command=self.signin)
        self.signin_button.pack(pady=5)

        self.signup_button = tk.Button(self, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=5)

    def signin(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect('course_reservation.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            if user[1] == 'admin':
                self.master.show_admin_page()
            else:
                self.master.show_user_page(user[0])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        self.master.destroy()
        signup_window = SignupPage()
        signup_window.mainloop()

# Sign Up Page
class SignupPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sign Up")
        self.geometry("300x400")
        self.create_widgets()

    def create_widgets(self):
        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.label_name = tk.Label(self, text="Name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        self.label_age = tk.Label(self, text="Age:")
        self.label_age.pack()
        self.entry_age = tk.Entry(self)
        self.entry_age.pack()

        self.label_qualification = tk.Label(self, text="Qualification:")
        self.label_qualification.pack()
        self.entry_qualification = tk.Entry(self)
        self.entry_qualification.pack()

        self.label_percentage = tk.Label(self, text="Percentage:")
        self.label_percentage.pack()
        self.entry_percentage = tk.Entry(self)
        self.entry_percentage.pack()

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        self.label_payment_mode = tk.Label(self, text="Payment Mode:")
        self.label_payment_mode.pack()
        self.entry_payment_mode = tk.Entry(self)
        self.entry_payment_mode.pack()

        self.signup_button = tk.Button(self, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=5)

    def signup(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        name = self.entry_name.get()
        age = self.entry_age.get()
        qualification = self.entry_qualification.get()
        percentage = self.entry_percentage.get()
        email = self.entry_email.get()
        payment_mode = self.entry_payment_mode.get()

        conn = sqlite3.connect('course_reservation.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, "user"))
            user_id = cursor.lastrowid
            cursor.execute("INSERT INTO personal_details (user_id, name, age, qualification, percentage, email, payment_mode) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, name, age, qualification, percentage, email, payment_mode))
            conn.commit()
            messagebox.showinfo("Success", "Sign up successful! You can now sign in.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        conn.close()
        self.destroy()

# User Page
class UserPage(tk.Frame):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.create_widgets()

    def create_widgets(self):
        self.label_welcome = tk.Label(self, text="Welcome User!")
        self.label_welcome.pack()

        self.view_courses_button = tk.Button(self, text="View Available Courses", command=self.view_courses)
        self.view_courses_button.pack(pady=10)

        self.view_personal_details_button = tk.Button(self, text="View Personal Details", command=self.view_personal_details)
        self.view_personal_details_button.pack(pady=10)

    def view_courses(self):
        # Display available courses and allow the user to select and reserve them
        self.master.withdraw()  # Hide the user page while viewing courses

        # Available courses
        courses = ["Python", "Java", "Web Developer", "Software Developer"]

        # Create a new window to display courses
        course_window = tk.Toplevel(self.master)
        course_window.title("Available Courses")
        course_window.geometry("300x200")

        # Display course options
        tk.Label(course_window, text="Select Course:").pack(pady=5)
        selected_course = tk.StringVar()
        selected_course.set(courses[0])  # Default value
        for course in courses:
            tk.Radiobutton(course_window, text=course, variable=selected_course, value=course).pack()

        # Reserve button
        tk.Button(course_window, text="Reserve", command=lambda: self.reserve_course(selected_course.get(), course_window)).pack(pady=10)

    def reserve_course(self, course, window):
        conn = sqlite3.connect('course_reservation.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservations (user_id, course_name) VALUES (?, ?)", (self.user_id, course))
        conn.commit()
        conn.close()
        messagebox.showinfo("Course Reserved", f"You have successfully reserved {course}!")
        window.destroy()
        self.master.deiconify()  # Show the user page again

    def view_personal_details(self):
        conn = sqlite3.connect('course_reservation.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, age, qualification, percentage, email, payment_mode FROM personal_details WHERE user_id = ?", (self.user_id,))
        personal_details = cursor.fetchone()
        conn.close()

        if personal_details:
            messagebox.showinfo("Personal Details", f"Name: {personal_details[0]}\nAge: {personal_details[1]}\nQualification: {personal_details[2]}\nPercentage: {personal_details[3]}\nEmail: {personal_details[4]}\nPayment Mode: {personal_details[5]}")
        else:
            messagebox.showinfo("Personal Details", "No personal details found.")

# Admin Page
class AdminPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label_welcome = tk.Label(self, text="Welcome Admin!")
        self.label_welcome.pack()

        self.label_email = tk.Label(self, text="Enter Candidate's Email ID:")
        self.label_email.pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        self.view_details_button = tk.Button(self, text="View Details", command=self.view_details)
        self.view_details_button.pack(pady=5)

        self.details_text = tk.Text(self, height=10, width=50)
        self.details_text.pack(fill=tk.BOTH, expand=True)

    def view_details(self):
        email = self.entry_email.get()

        conn = sqlite3.connect('course_reservation.db')
        cursor = conn.cursor()
        cursor.execute("SELECT p.name, p.age, p.qualification, p.percentage, p.email, p.payment_mode, r.course_name FROM personal_details p LEFT JOIN reservations r ON p.user_id = r.user_id WHERE p.email = ?", (email,))
        details = cursor.fetchone()
        conn.close()

        if details:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Name: {details[0]}\nAge: {details[1]}\nQualification: {details[2]}\nPercentage: {details[3]}\nEmail: {details[4]}\nPayment Mode: {details[5]}\nReserved Course: {details[6]}")
        else:
            messagebox.showinfo("Details", "No details found for the provided email ID.")

if __name__ == "__main__":
    app = CourseReservationApp()
    app.mainloop()
