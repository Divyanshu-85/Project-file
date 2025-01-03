import mysql.connector

# Establish connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="your_username",      # replace with your MySQL username
    password="your_password",  # replace with your MySQL password
    database="login_db"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Function to register a new user
def register(username, password):
    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        db.commit()
        print("Registration successful!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to change user credentials
def change_credentials(old_username, new_username, new_password):
    try:
        query = "UPDATE users SET username = %s, password = %s WHERE username = %s"
        cursor.execute(query, (new_username, new_password, old_username))
        db.commit()
        print("Credentials updated successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Main loop for user interaction
while True:
    print("\n1. Login")
    print("2. Register")
    print("3. Change Username/Password")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Check if the user exists
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            print(f"Login successful! Welcome, {username}.")
        else:
            print("Invalid credentials. Please try again.")

    elif choice == '2':
        username = input("Choose a username: ")
        password = input("Choose a password: ")
        register(username, password)

    elif choice == '3':
        old_username = input("Enter your current username: ")
        new_username = input("Enter a new username: ")
        new_password = input("Enter a new password: ")
        change_credentials(old_username, new_username, new_password)

    elif choice == '4':
        break

    else:
        print("Invalid option. Please try again.")

# Close the cursor and database connection
cursor.close()
db.close()
