import sqlite3

# Connect to the medio database
conn = sqlite3.connect('medio.db')

# Create a cursor object to interact with the database
cur = conn.cursor()

# Define a function to create the request table
def create_request_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS request
                   (request_num INTEGER PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    phone_num TEXT NOT NULL,
                    address TEXT NOT NULL,
                    plastic_type TEXT NOT NULL)''')
    conn.commit()

# Define a function to create the user table
def create_user_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                   (user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL)''')
    conn.commit()

# Call the create_request_table and create_user_table functions to create the tables
create_request_table()
create_user_table()

# Define a function to add a new request to the request table
def add_request():
    # Collect information from the user
    customer_name = input("Enter customer name: ")
    phone_num = input("Enter phone number: ")
    address = input("Enter address: ")
    plastic_type = input("Enter plastic type: ")
    
    # Check if the customer is already in the user table
    cur.execute("SELECT * FROM users WHERE name=?", (customer_name,))
    user = cur.fetchone()
    if not user:
        # If the customer is not in the user table, add them
        cur.execute("INSERT INTO users (name) VALUES (?)", (customer_name,))
        conn.commit()
        user_id = cur.lastrowid
    else:
        user_id = user[0]
    
    # Add the new request to the request table
    cur.execute("INSERT INTO request (customer_name, phone_num, address, plastic_type) VALUES (?, ?, ?, ?)", (customer_name, phone_num, address, plastic_type))
    conn.commit()
    request_num = cur.lastrowid
    
    print(f"New request added with request number {request_num}")

# Define a function to update the address of a request
def update_address():
    # Collect information from the user
    request_num = input("Enter request number: ")
    new_address = input("Enter new address: ")
    
    # Update the address in the request table
    cur.execute("UPDATE request SET address=? WHERE request_num=?", (new_address, request_num))
    conn.commit()
    
    print(f"Address for request {request_num} updated to {new_address}")

# Define a function to view the details of a request
def view_request():
    # Collect information from the user
    request_num = input("Enter request number: ")
    
    # Get the row from the request table with the corresponding request number
    cur.execute("SELECT * FROM request WHERE request_num=?", (request_num,))
    row = cur.fetchone()
    if row:
        print(f"Request number: {row[0]}")
        print(f"Customer name: {row[1]}")
        print(f"Phone number: {row[2]}")
        print(f"Address: {row[3]}")
        print(f"Plastic type: {row[4]}")
    else:
        print(f"Request number {request_num} not found")

def view_all_requests():
    # Get all the rows from the request table
    cur.execute("SELECT * FROM request")
    rows = cur.fetchall()
    
    # Print the details of each request
    if rows:
        for row in rows:
            print(f"Request number: {row[0]}")
            print(f"Customer name: {row[1]}")
            print(f"Phone number: {row[2]}")
            print(f"Address: {row[3]}")
            print(f"Plastic type: {row[4]}")
            print()
    else:
        print("No requests found")

# Define a function to delete a request
def delete_request():
    # Collect information from the user
    request_num = input("Enter request number: ")
    
    # Delete the row from the request table with the corresponding request number
    cur.execute("DELETE FROM request WHERE request_num=?", (request_num,))
    conn.commit()
    
    print("Request deleted")

def calculate_contributions():
    # Collect information from the user
    customer_name = input("Enter customer name: ")
    cur.execute("SELECT user_id FROM users WHERE name=?", (customer_name,))
    user_id = cur.fetchone()
    if user_id:
        user_id = user_id[0]
    
        # Get the number of requests made by the user from the request table
        cur.execute("SELECT COUNT(*) FROM request WHERE customer_name=?", (customer_name,))
        num_requests = cur.fetchone()[0]
    
        print(f"{customer_name} has made {num_requests} contributions")
    else:
        print(f"{customer_name} not found in the user database")


# Import necessary modules and functions

# Define the menu function
def menu():
    print("Choose an option:")
    print("1. Request a pickup")
    print("2. Change address")
    print("3. View request details")
    print("4. Delete request")
    print("5. View all requests")
    print("6. See your contributions")
    print("0. Exit")

    # Collect the user's choice
    choice = input("Enter the number of your choice: ")

    # Call the appropriate function based on the user's choice
    if choice == "1":
        add_request()
    elif choice == "2":
        update_address()
    elif choice == "3":
        view_request()
    elif choice == "4":
        delete_request()
    elif choice == "5":
        view_all_requests()
    elif choice == "6":
        calculate_contributions()
    elif choice == "0":
        exit()
    else:
        print("Invalid choice. Please enter a number from 0 to 4.")

# Call the menu function in a loop until the user chooses to exit
while True:
    menu()
