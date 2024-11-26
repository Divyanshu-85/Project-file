import os
import shutil
import mysql.connector
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog, Listbox, StringVar, simpledialog


# Establish connection to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        port=330,
        password="Hacker@85",
        database="server"
    )


# Initialize the database
def initialize_database():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            file_path VARCHAR(255) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    connection.commit()
    connection.close()


# GUI for the app
class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("400x500")

        # Set background and text colors
        self.root.configure(bg="black")
        self.bg_color = "black"
        self.text_color = "red"
        self.border_color = "green"

        # Variables
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.current_user = None

        # Welcome screen
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_screen()
        Label(self.root, text="File Manager", font=("Arial", 18), bg=self.bg_color, fg=self.text_color).pack(pady=20)
        Button(self.root, text="Register", command=self.show_register_screen, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Login", command=self.show_login_screen, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Exit", command=self.root.quit, bg=self.border_color, fg=self.text_color).pack(pady=10)

    def show_register_screen(self):
        self.clear_screen()
        Label(self.root, text="Register", font=("Arial", 16), bg=self.bg_color, fg=self.text_color).pack(pady=20)
        Label(self.root, text="Username", bg=self.bg_color, fg=self.text_color).pack()
        Entry(self.root, textvariable=self.username_var, bg=self.bg_color, fg=self.text_color).pack(pady=5)
        Label(self.root, text="Password", bg=self.bg_color, fg=self.text_color).pack()
        Entry(self.root, textvariable=self.password_var, show="*", bg=self.bg_color, fg=self.text_color).pack(pady=5)
        Button(self.root, text="Register", command=self.register_user, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Back", command=self.show_welcome_screen, bg=self.border_color, fg=self.text_color).pack(pady=5)

    def register_user(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        connection = connect_to_db()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_welcome_screen()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            connection.close()

    def show_login_screen(self):
        self.clear_screen()
        Label(self.root, text="Login", font=("Arial", 16), bg=self.bg_color, fg=self.text_color).pack(pady=20)
        Label(self.root, text="Username", bg=self.bg_color, fg=self.text_color).pack()
        Entry(self.root, textvariable=self.username_var, bg=self.bg_color, fg=self.text_color).pack(pady=5)
        Label(self.root, text="Password", bg=self.bg_color, fg=self.text_color).pack()
        Entry(self.root, textvariable=self.password_var, show="*", bg=self.bg_color, fg=self.text_color).pack(pady=5)
        Button(self.root, text="Login", command=self.login_user, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Back", command=self.show_welcome_screen, bg=self.border_color, fg=self.text_color).pack(pady=5)

    def login_user(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            self.current_user = user
            messagebox.showinfo("Success", "Login successful!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def show_dashboard(self):
        self.clear_screen()
        Label(self.root, text=f"Welcome, {self.current_user['username']}", font=("Arial", 16), bg=self.bg_color, fg=self.text_color).pack(pady=20)
        Button(self.root, text="Upload File", command=self.upload_file, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="View Files", command=self.view_files, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Search Files", command=self.search_files, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Download File", command=self.download_file, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Change Username", command=self.change_username, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Change Password", command=self.change_password, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Delete Account", command=self.delete_account, bg=self.border_color, fg=self.text_color).pack(pady=10)
        Button(self.root, text="Logout", command=self.show_welcome_screen, bg=self.border_color, fg=self.text_color).pack(pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            file_name = os.path.basename(file_path)
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO documents (user_id, file_name, file_path) VALUES (%s, %s, %s)",
                (self.current_user['id'], file_name, file_path)
            )
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "File uploaded successfully!")

    def view_files(self):
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT file_name FROM documents WHERE user_id=%s", (self.current_user['id'],))
        files = cursor.fetchall()
        connection.close()

        self.clear_screen()
        Label(self.root, text="Your Files", font=("Arial", 16), bg=self.bg_color, fg=self.text_color).pack(pady=20)
        file_list = Listbox(self.root, bg=self.bg_color, fg=self.text_color)
        file_list.pack(pady=10, fill="both", expand=True)
        for file in files:
            file_list.insert("end", file['file_name'])
        Button(self.root, text="Back", command=self.show_dashboard, bg=self.border_color, fg=self.text_color).pack(pady=10)

    def search_files(self):
        search_term = simpledialog.askstring("Search File", "Enter the file name to search:")
        if not search_term:
            return

        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT file_name FROM documents WHERE user_id=%s AND file_name LIKE %s",
            (self.current_user['id'], f"%{search_term}%")
        )
        files = cursor.fetchall()
        connection.close()

        if files:
            results = "\n".join(file['file_name'] for file in files)
            messagebox.showinfo("Search Results", results)
        else:
            messagebox.showinfo("Search Results", "No matching files found.")

    def download_file(self):
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM documents WHERE user_id=%s", (self.current_user['id'],))
        files = cursor.fetchall()
        connection.close()

        if not files:
            messagebox.showinfo("No Files", "You have no files to download.")
            return

        file_list = [file['file_name'] for file in files]
        selected_file = simpledialog.askstring("Download File", f"Select a file to download:\n{', '.join(file_list)}")
        if not selected_file:
            return

        for file in files:
            if file['file_name'] == selected_file:
                destination_path = filedialog.askdirectory(title="Select Destination")
                if destination_path:
                    shutil.copy(file['file_path'], os.path.join(destination_path, file['file_name']))
                    messagebox.showinfo("Success", f"File '{selected_file}' downloaded successfully!")
                break
        else:
            messagebox.showerror("Error", "File not found.")

    def change_username(self):
        new_username = simpledialog.askstring("Change Username", "Enter a new username:")
        if not new_username:
            return

        connection = connect_to_db()
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE users SET username=%s WHERE id=%s", (new_username, self.current_user['id']))
            connection.commit()
            self.current_user['username'] = new_username
            messagebox.showinfo("Success", "Username updated successfully!")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            connection.close()

    def change_password(self):
        new_password = simpledialog.askstring("Change Password", "Enter a new password:", show="*")
        if not new_password:
            return

        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_password, self.current_user['id']))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Password updated successfully!")

    def delete_account(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
        if not confirm:
            return

        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (self.current_user['id'],))
        connection.commit()
        connection.close()
        self.current_user = None
        messagebox.showinfo("Success", "Account deleted successfully!")
        self.show_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Main Application
def main():
    initialize_database()
    root = Tk()
    app = FileManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
