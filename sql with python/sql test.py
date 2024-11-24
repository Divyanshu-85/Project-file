import pyttsx3
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    port=330, 
    user = "root",
    password = "Hacker@85",
    database ="login"
)
b = mydb.cursor()
def speak(message, username=""):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    
    if username:
        message += f" {username}"
        
    engine.say(message)
    engine.runAndWait()

input_username = input("Enter your username:- ")
input_password = input("Enter your password:- ")

# SQL query to fetch the user data
query = "SELECT * FROM account WHERE username = %s AND Password = %s"
values = (input_username, input_password)

# Execute the query
b.execute(query, values)
result = b.fetchone()  # Fetch one matching record

# Validation logic
if result:
    speak("Access granted! Welcome,", input_username)
    # Provide options to modify account
    option = input("Do you want to change your username, password, or delete your account? (username/password/delete/none): ").lower()
    if option == "username":
        new_username = input("Enter your new username: ")
        update_query = "UPDATE account SET username = %s WHERE username = %s AND Password = %s"
        b.execute(update_query, (new_username, input_username, input_password))
        mydb.commit()
        speak("Username updated successfully!")
    elif option == "password":
        new_password = input("Enter your new password: ")
        update_query = "UPDATE account SET Password = %s WHERE username = %s AND Password = %s"
        b.execute(update_query, (new_password, input_username, input_password))
        mydb.commit()
        speak("Password updated successfully!")
        
    elif option == "delete":
        confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
        if confirm == "yes":
            delete_query = "DELETE FROM account WHERE username = %s AND Password = %s"
            b.execute(delete_query, (input_username, input_password))
            mydb.commit()
            speak("Account deleted successfully!")
            
        else:
            speak("Account deletion canceled.")            
    else:
        speak("No changes made.")        
else:
    speak("Access denied! Incorrect username or password.")    
q = input("Do you want to login with new id:- ")
if q == "yes":
    s = "insert into account (username, Password) values(%s, %s)"
    Username = input("Enter new username:- ")
    Password = input("Enter new Password:- ")
    b1 = [(Username, Password)]
    b.executemany(s, b1)
    mydb.commit()    
else:
    speak("Ok, Thankyou")
  
