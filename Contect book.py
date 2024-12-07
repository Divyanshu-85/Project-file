import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "port": 330,
    "password": "Hacker@85",  # Replace with your MySQL password
    "database": "ContactManager"
}

# Connect to MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Contact Management Functions
def add_contact(name, phone, email):
    connection = connect_to_db()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Contacts (Name, Phone, Email) VALUES (%s, %s, %s)", (name, phone, email))
        connection.commit()
        return "Contact added successfully!"
    except Error as e:
        return f"Error: {e}"
    finally:
        connection.close()

def search_contact(query):
    connection = connect_to_db()
    if not connection:
        return
    try:
        cursor = connection.cursor(dictionary=True)
        query = f"%{query}%"
        cursor.execute("SELECT * FROM Contacts WHERE Name LIKE %s OR Phone LIKE %s OR Email LIKE %s", (query, query, query))
        results = cursor.fetchall()
        return results if results else "No matching contacts found."
    except Error as e:
        return f"Error: {e}"
    finally:
        connection.close()

def get_all_contacts():
    connection = connect_to_db()
    if not connection:
        return
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Contacts")
        results = cursor.fetchall()
        return results if results else "No contacts found."
    except Error as e:
        return f"Error: {e}"
    finally:
        connection.close()

# GUI Implementation
def add_contact_gui():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    
    if not (name and phone and email):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    result = add_contact(name, phone, email)
    messagebox.showinfo("Result", result)
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def search_contact_gui():
    query = entry_search.get()
    if not query:
        messagebox.showerror("Error", "Search field cannot be empty!")
        return
    
    results = search_contact(query)
    if isinstance(results, str):
        messagebox.showinfo("Result", results)
    else:
        display_results(results)

def display_results(results):
    for row in tree.get_children():
        tree.delete(row)
    for contact in results:
        tree.insert("", tk.END, values=(contact["Name"], contact["Phone"], contact["Email"]))

def show_all_contacts_gui():
    results = get_all_contacts()
    if isinstance(results, str):
        messagebox.showinfo("Result", results)
    else:
        display_results(results)

# Initialize GUI window
root = tk.Tk()
root.title("Contact Manager")
root.geometry("600x400")

# Add Contact Section
tk.Label(root, text="Add Contact").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(root, text="Name:").grid(row=1, column=0, padx=5, sticky="e")
tk.Label(root, text="Phone:").grid(row=2, column=0, padx=5, sticky="e")
tk.Label(root, text="Email:").grid(row=3, column=0, padx=5, sticky="e")

entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=5, pady=5)
entry_phone = tk.Entry(root)
entry_phone.grid(row=2, column=1, padx=5, pady=5)
entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1, padx=5, pady=5)

tk.Button(root, text="Add Contact", command=add_contact_gui).grid(row=4, column=0, columnspan=2, pady=10)

# Search Section
tk.Label(root, text="Search Contacts").grid(row=0, column=2, columnspan=2, pady=10)
entry_search = tk.Entry(root)
entry_search.grid(row=1, column=2, padx=5, pady=5)
tk.Button(root, text="Search", command=search_contact_gui).grid(row=2, column=2, columnspan=2, pady=10)

# Display Section
tree = ttk.Treeview(root, columns=("Name", "Phone", "Email"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

tk.Button(root, text="Show All Contacts", command=show_all_contacts_gui).grid(row=6, column=0, columnspan=4, pady=10)

root.mainloop()
