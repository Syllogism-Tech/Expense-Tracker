# database.py
import sqlite3

def create_connection():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    return conn

def add_expense(conn, date, category, description, amount):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()

def get_expenses(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    return cursor.fetchall()

def get_total_expense(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()
    return total[0] if total[0] else 0.0

# expense_tracker.py
import tkinter as tk
from tkinter import ttk
from database import create_connection, add_expense, get_expenses, get_total_expense

def add_expense_button_click():
    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    amount = float(amount_entry.get())

    add_expense(conn, date, category, description, amount)
    update_expense_list()
    clear_input_fields()

def update_expense_list():
    expense_tree.delete(*expense_tree.get_children())
    expenses = get_expenses(conn)
    for expense in expenses:
        expense_tree.insert("", "end", values=expense)

def clear_input_fields():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")

# Create database connection
conn = create_connection()

# Create widgets
date_label = tk.Label(root, text="Date:")
date_entry = tk.Entry(root)
category_label = tk.Label(root, text="Category:")
category_entry = tk.Entry(root)
description_label = tk.Label(root, text="Description:")
description_entry = tk.Entry(root)
amount_label = tk.Label(root, text="Amount:")
amount_entry = tk.Entry(root)
add_expense_button = tk.Button(root, text="Add Expense", command=add_expense_button_click)

# Create expense list treeview
expense_tree = ttk.Treeview(root, columns=("ID", "Date", "Category", "Description", "Amount"))
expense_tree.heading("#1", text="ID")
expense_tree.heading("#2", text="Date")
expense_tree.heading("#3", text="Category")
expense_tree.heading("#4", text="Description")
expense_tree.heading("#5", text="Amount")
expense_tree.column("#1", width=40)
expense_tree.column("#2", width=100)
expense_tree.column("#3", width=100)
expense_tree.column("#4", width=200)
expense_tree.column("#5", width=100)
update_expense_list()

# Layout widgets
date_label.grid(row=0, column=0)
date_entry.grid(row=0, column=1)
category_label.grid(row=1, column=0)
category_entry.grid(row=1, column=1)
description_label.grid(row=2, column=0)
description_entry.grid(row=2, column=1)
amount_label.grid(row=3, column=0)
amount_entry.grid(row=3, column=1)
add_expense_button.grid(row=4, column=0, columnspan=2)
expense_tree.grid(row=5, column=0, columnspan=2)

# Start the GUI main loop
root.mainloop()
