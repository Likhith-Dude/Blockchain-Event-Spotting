import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import string

DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def register_user(username, password, email):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                       (username, password, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Event Spotting - Auth")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        init_db()
        self.show_login()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()
        tk.Label(self.root, text="Login", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.root, text="Username:").pack()
        self.login_user = tk.Entry(self.root, width=30)
        self.login_user.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()
        self.login_pass = tk.Entry(self.root, show="*", width=30)
        self.login_pass.pack(pady=5)

        tk.Button(self.root, text="Login", width=20, command=self.do_login,
                  bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.root, text="Register", width=20, command=self.show_register).pack()

    def show_register(self):
        self.clear_frame()
        tk.Label(self.root, text="Register", font=("Arial", 18, "bold")).pack(pady=15)

        tk.Label(self.root, text="Username:").pack()
        self.reg_user = tk.Entry(self.root, width=30)
        self.reg_user.pack(pady=4)

        tk.Label(self.root, text="Email:").pack()
        self.reg_email = tk.Entry(self.root, width=30)
        self.reg_email.pack(pady=4)

        tk.Label(self.root, text="Password:").pack()
        self.reg_pass = tk.Entry(self.root, show="*", width=30)
        self.reg_pass.pack(pady=4)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Generate Password", command=self.fill_generated_pass,
                  bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Register", command=self.do_register,
                  bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Back to Login", command=self.show_login).pack(pady=5)

    def fill_generated_pass(self):
        pwd = generate_password()
        self.reg_pass.delete(0, tk.END)
        self.reg_pass.insert(0, pwd)
        messagebox.showinfo("Generated Password", f"Your password: {pwd}\nPlease save it!")

    def do_login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()
        if validate_login(username, password):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def do_register(self):
        username = self.reg_user.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_pass.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return
        if register_user(username, password, email):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists.")

if __name__ == '__main__':
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()
