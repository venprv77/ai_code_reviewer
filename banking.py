import MySQLdb


class Bank:

    def __init__(self):

        # Connect to MySQL
        self.con = MySQLdb.connect(
            host="localhost",
            user="root",
            password="moksha"
        )

        self.cursor = self.con.cursor()

        # Create Database
        sql = "CREATE DATABASE IF NOT EXISTS bank_db"
        self.cursor.execute(sql)

        # Select Database
        self.cursor.execute("USE bank_db")

        # Create Table
        sql = """
        CREATE TABLE IF NOT EXISTS account (
            acc_no INT PRIMARY KEY,
            name VARCHAR(50),
            balance FLOAT
        )
        """

        self.cursor.execute(sql)

        self.con.commit()

        print("Database and table created successfully")


    # Create Account
    def create_account(self):

        acc_no = int(input("Enter Account Number: "))
        name = input("Enter Name: ")
        balance = float(input("Enter Initial Balance: "))

        sql = """
        INSERT INTO account(acc_no, name, balance)
        VALUES (%s, %s, %s)
        """

        self.cursor.execute(sql, (acc_no, name, balance))
        self.con.commit()

        print("Account created successfully")


    # Deposit Money
    def deposit(self):

        acc_no = int(input("Enter Account Number: "))
        amount = float(input("Enter Deposit Amount: "))

        sql = """
        UPDATE account
        SET balance = balance + %s
        WHERE acc_no = %s
        """

        self.cursor.execute(sql, (amount, acc_no))

        if self.cursor.rowcount > 0:

            self.con.commit()
            print("Amount deposited successfully")

        else:

            print("Account not found")


    # Withdraw Money
    def withdraw(self):

        acc_no = int(input("Enter Account Number: "))
        amount = float(input("Enter Withdraw Amount: "))

        # Check balance
        sql = "SELECT balance FROM account WHERE acc_no = %s"

        self.cursor.execute(sql, (acc_no,))

        result = self.cursor.fetchone()

        if result is None:

            print("Account not found")

        elif result[0] >= amount:

            sql = """
            UPDATE account
            SET balance = balance - %s
            WHERE acc_no = %s
            """

            self.cursor.execute(sql, (amount, acc_no))
            self.con.commit()

            print("Amount withdrawn successfully")

        else:

            print("Insufficient balance")


    # Check Balance
    def check_balance(self):

        acc_no = int(input("Enter Account Number: "))

        sql = """
        SELECT name, balance
        FROM account
        WHERE acc_no = %s
        """

        self.cursor.execute(sql, (acc_no,))

        result = self.cursor.fetchone()

        if result:

            print("Account Holder:", result[0])
            print("Balance:", result[1])

        else:

            print("Account not found")


    # Display All Accounts
    def display_accounts(self):

        sql = "SELECT * FROM account"

        self.cursor.execute(sql)

        rows = self.cursor.fetchall()

        if len(rows) == 0:

            print("No accounts available")

        else:

            print("\n----- ALL ACCOUNTS -----")

            for row in rows:

                print("Account Number:", row[0])
                print("Name:", row[1])
                print("Balance:", row[2])
                print("------------------------")


    # Close Connection
    def close_connection(self):

        self.cursor.close()
        self.con.close()

        print("Database connection closed")


# Create Bank Object
bank = Bank()


# Main Menu
while True:

    print("\n==============================")
    print("       BANK APPLICATION")
    print("==============================")

    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Display All Accounts")
    print("6. Exit")

    choice = int(input("Enter your choice: "))


    if choice == 1:

        bank.create_account()


    elif choice == 2:

        bank.deposit()


    elif choice == 3:

        bank.withdraw()


    elif choice == 4:

        bank.check_balance()


    elif choice == 5:

        bank.display_accounts()


    elif choice == 6:

        bank.close_connection()

        print("Thank you for using Bank Application")

        break


    else:

        print("Invalid choice")