import mysql.connector
from mysql.connector import Error
import getpass
import os
import claim_number
from password import PASSWORD
from mysqlDatabase import DATABASE
from user import USERNM
from host import HOST


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_connection(host, user, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Error as e:
        print(f"Error connecting to the database: {e}")
        input("Press Enter to continue...")
    return connection

def add_new_user(connection):
    clear_screen()
    print("\nAdd New User:")
    print("1. Add Customer")
    print("2. Add Agent")
    print("3. Add Admin")
    choice = input("Enter user type to add (1/2/3): ")

    if choice == '1':
        add_customer(connection)
    elif choice == '2':
        add_agent(connection)
    elif choice == '3':
        add_admin(connection)
    else:
        print("Invalid choice")

def add_customer(connection):
    clear_screen()
    print("\nAdd New Customer:")
    username = input("Enter username: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    address = input("Enter address: ")
    password = getpass.getpass("Enter password: ")

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO Customers (Username, FirstName, LastName, Email, Phone, Address, Password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (username, first_name, last_name, email, phone, address, password))
        connection.commit()
        print("Customer added successfully")

        cursor.execute("SELECT LAST_INSERT_ID()")
        customer_id = cursor.fetchone()[0]
        print("Customer ID:", customer_id)
        input("Press Enter to continue...")

    except Error as e:
        print(f"Error adding customer: {e}")
        input("Press Enter to continue...") 

def add_agent(connection):
    clear_screen()
    print("\nAdd New Agent:")
    username = input("Enter username: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    password = getpass.getpass("Enter password: ")

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO InsuranceAgents (Username, FirstName, LastName, Email, Phone, Password) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (username, first_name, last_name, email, phone, password))
        connection.commit()
        print("Agent added successfully")

        # Get the AgentID of the added agent
        cursor.execute("SELECT LAST_INSERT_ID()")
        agent_id = cursor.fetchone()[0]
        print("Agent ID:", agent_id)
        input("Press Enter to continue...")

    except Error as e:
        print(f"Error adding agent: {e}")
        input("Press Enter to continue...")

def add_admin(connection):
    clear_screen()
    print("\nAdd New Admin:")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO Admins (Username, Password) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))
        connection.commit()
        print("Admin added successfully")
        input("Press Enter to continue...")
    except Error as e:
        print(f"Error adding admin: {e}")

def admin_login(connection):
    clear_screen()
    print("\nAdmin Login:")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM Admins WHERE Username = %s AND Password = %s"
        cursor.execute(sql, (username, password))
        admin = cursor.fetchone()
        if admin:
            print("Login successful")
            input("Press Enter to continue...")
            return admin[0]
        else:
            print("Invalid username or password")
            input("Press Enter to continue...")
            return None
    except Error as e:
        print(f"Error logging in as admin: {e}")
        input("Press Enter to continue...")
        return None

def agent_login(connection):
    clear_screen()
    print("\nAgent Login:")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM InsuranceAgents WHERE Username = %s AND Password = %s"
        cursor.execute(sql, (username, password))
        agent = cursor.fetchone()
        if agent:
            print("Login successful")
            input("Press Enter to continue...")
            return agent[0]
        else:
            print("Invalid username or password")
            input("Press Enter to continue...")
            return None
    except Error as e:
        print(f"Error logging in as agent: {e}")
        input("Press Enter to continue...")
        return None

def customer_login(connection):
    clear_screen()
    print("\nCustomer Login:")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM Customers WHERE Username = %s AND Password = %s"
        cursor.execute(sql, (username, password))
        customer = cursor.fetchone()
        if customer:
            print("Login successful")
            input("Press Enter to continue...")
            return customer[0]
        else:
            print("Invalid username or password")
            input("Press Enter to continue...")
            return None
    except Error as e:
        print(f"Error logging in as customer: {e}")
        input("Press Enter to continue...")
        return None
    
def view_policies(connection, user_id=None, is_agent=False):
    try:
        cursor = connection.cursor()

        if is_agent:
            sql = "SELECT * FROM `insurance_system`.`insurancepolicies` WHERE PolicyID IN (SELECT PolicyID FROM PolicyAssignments WHERE AgentID = %s)"
            cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT * FROM `insurance_system`.`insurancepolicies`"
            cursor.execute(sql)

        policies = cursor.fetchall()

        if not policies:
            print("No policies found")
            input("Press Enter to continue...")
        else:
            for policy in policies:
                print(policy)
            input("Press Enter to continue...")
    except Error as e:
        print(f"Error viewing policies: {e}")
        input("Press Enter to continue...")

def add_policy(connection):
    clear_screen()
    print("\nAdd Policy:")
    policy_number = input("Enter Policy Number: ")
    policy_type = input("Enter Policy Type: ")
    start_date = input("Enter Policy Start Date (YYYY-MM-DD): ")
    end_date = input("Enter Policy End Date (YYYY-MM-DD): ")
    premium_amount = float(input("Enter Premium Amount: "))

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO `insurance_system`.`insurancepolicies` (PolicyNumber, PolicyType, PolicyStartDate, PolicyEndDate, PremiumAmount) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (policy_number, policy_type, start_date, end_date, premium_amount))
        connection.commit()
        print("Policy added successfully")
        input("Press Enter to continue...")
    except Error as e:
        print(f"Error adding policy: {e}")
        input("Press Enter to continue...")

def make_claim(connection, customer_id):
    clear_screen()
    print("\nMake a Claim:")
    policy_number = input("Enter Policy Number: ")
    claim_amount = float(input("Enter Claim Amount: "))

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO Claims (ClaimDate, ClaimAmount, PolicyID) VALUES (CURDATE(), %s, (SELECT PolicyID FROM PolicyOwnership WHERE CustomerID = %s AND PolicyID = (SELECT PolicyID FROM `insurance_system`.`insurancepolicies` WHERE PolicyNumber = %s)))"
        cursor.execute(sql, (claim_amount, customer_id, policy_number))
        connection.commit()
        print("Claim made successfully")
        cursor.execute("SELECT LAST_INSERT_ID()")
        claim_id = cursor.fetchone()[0]
        print("Claim ID:", claim_id)
        input("Press Enter to continue...")
    except Error as e:
        print(f"Error making claim: {e}")
        input("Press Enter to continue...")

def approve_claim(connection):
    clear_screen()
    print("\nApprove a Claim:")
    claim_id = input("Enter Claim ID: ")

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Claims WHERE ClaimID = %s", (claim_id,))
        claim_exists = cursor.fetchone()[0]
        if claim_exists:
            sql = "UPDATE Claims SET Approved = 1 WHERE ClaimID = %s"
            cursor.execute(sql, (claim_id,))
            connection.commit()
            print("Claim approved successfully")
        else:
            print("Claim ID does not exist")
        input("Press Enter to continue...")
    except Error as e:
        print(f"Error approving claim: {e}")
        input("Press Enter to continue...")

def assign_policy(connection):
    clear_screen()
    print("\nAssign a Policy:")
    policy_number = input("Enter Policy Number: ")
    customer_id = int(input("Enter Customer ID: "))

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO PolicyOwnership (CustomerID, PolicyID) VALUES (%s, (SELECT PolicyID FROM `insurance_system`.`insurancepolicies` WHERE PolicyNumber = %s))"
        cursor.execute(sql, (customer_id, policy_number))
        connection.commit()
        print("Policy assigned successfully")
        input("Press Enter to continue...")
    except Error as e:
        print(f"Error assigning policy: {e}")
        input("Press Enter to continue...")

def view_claims(connection):
    clear_screen()
    print("\nView Claims:")
    customer_id = input("Enter Customer ID or leave blank for all claims: ")

    try:
        cursor = connection.cursor()
        if customer_id:
            sql = "SELECT * FROM Claims WHERE PolicyID IN (SELECT PolicyID FROM PolicyOwnership WHERE CustomerID = %s)"
            cursor.execute(sql, (customer_id,))
        else:
            sql = "SELECT * FROM Claims"
            cursor.execute(sql) 
        claims = cursor.fetchall()
        if not claims:
            print("No claims found")
            input("Press Enter to continue...")
        else:
            for claim in claims:
                print(claim)
            input("Press Enter to continue...")
    except Error as e:
        print(f"Error viewing claims: {e}")
        input("Press Enter to continue...")

def view_customer_details(connection):
    clear_screen()
    print("\nView Customer Details:")
    customer_id = input("Enter Customer ID: ")

    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM Customers WHERE CustomerID = %s"
        cursor.execute(sql, (customer_id,))
        customer = cursor.fetchone()

        if customer:
            print("Customer ID:", customer[0])
            print("Username:", customer[1])
            print("First Name:", customer[2])
            print("Last Name:", customer[3])
            print("Email:", customer[4])
            print("Phone:", customer[5])
            print("Address:", customer[6])
            input("Press Enter to continue...")
        else:
            print("Customer not found")
            input("Press Enter to continue...")
    except Error as e:
        print(f"Error viewing customer details: {e}")
        input("Press Enter to continue...")

def view_agent_details(connection):
    clear_screen()
    print("\nView Agent Details:")
    agent_id = input("Enter Agent ID: ")

    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM InsuranceAgents WHERE AgentID = %s"
        cursor.execute(sql, (agent_id,))
        agent = cursor.fetchone()

        if agent:
            print("Agent ID:", agent[0])
            print("Username:", agent[1])
            print("First Name:", agent[2])
            print("Last Name:", agent[3])
            print("Email:", agent[4])
            print("Phone:", agent[5])
            input("Press Enter to continue...")
        else:
            print("Agent not found")
            input("Press Enter to continue...")
    except Error as e:
        print(f"Error viewing agent details: {e}")
        input("Press Enter to continue...")

def view_user_details(connection):
    clear_screen()
    print("\nView User Details:")
    user_type = input("Enter user type (1 for Customer, 2 for Agent): ")

    if user_type == '1':
        view_customer_details(connection)
    elif user_type == '2':
        view_agent_details(connection)
    else:
        print("Invalid choice")

def customer_menu(connection, customer_id):
    while True:
        clear_screen()
        print("\nCustomer Menu:")
        print("1. View Policies")
        print("2. Make a Claim")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_policies(connection, customer_id)
        elif choice == '2':
            make_claim(connection, customer_id)
        elif choice == '3':
            break
        else:
            print("Invalid choice")

def agent_menu(connection, agent_id):
    while True:
        clear_screen()
        print("\nAgent Menu:")
        print("1. Approve Claims")
        print("2. Assign Policy")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            approve_claim(connection)
        elif choice == '2':
            assign_policy(connection)
        elif choice == '3':
            break
        else:
            print("Invalid choice")

def admin_menu(connection, admin_id):
    while True:
        clear_screen()
        print("\nAdmin Menu:")
        print("1. View Policies")
        print("2. Add Policy")
        print("3. View Claims")
        print("4. View Customer/Agent Details")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_policies(connection)
        elif choice == '2':
            add_policy(connection)
        elif choice == '3':
            view_claims(connection)
        elif choice == '4':
            view_user_details(connection)
        elif choice == '5':
            break
        else:
            print("Invalid choice")

def main_menu(connection):
    clear_screen()
    print("\nMain Menu:")
    print("1. Customers")
    print("2. Agents")
    print("3. Admins")
    print("4. Add New User")
    print("5. Exit")
    choice = input("Enter your choice: ")
    return choice

def main(connection):
    while True:
        choice = main_menu(connection)

        if choice == '1':
            customer_id = customer_login(connection)
            if customer_id:
                customer_menu(connection, customer_id)
        elif choice == '2':
            agent_id = agent_login(connection)
            if agent_id:
                agent_menu(connection, agent_id)
        elif choice == '3':
            admin_id = admin_login(connection)
            if admin_id:
                admin_menu(connection, admin_id)
        elif choice == '4':
            add_new_user(connection)
        elif choice == '5':
            break
        else:
            print("Invalid choice")

    connection.close()
    clear_screen()
    print("Exited Successfully")

if __name__ == "__main__":
    connection = create_connection(HOST, USERNM, PASSWORD, DATABASE)
    if connection is not None:
        main(connection)
    else:
        clear_screen()
        print("Error: Unable to connect to the database")