from pymysql import connect
import hashlib
import os

connection = connect(
    host = os.getenv("MYSQL_HOST"),
    user = os.getenv("MYSQL_USER"),
    password = os.getenv("MYSQL_PASSWORD"),
    db = os.getenv("MYSQL_DATABASE"),
    charset = "UTF8mb4"
    )

account_id = 0
userInput = 0


try:
    while True:
        print("1. login")
        print("2. create")
        print("3. exit")
        userInput = int(input())

        if userInput == 1:
            print("Loging in...")
            login = input("login: ")
            password = input("password: ")

            password = bytes(password, "utf-8")
            hash_password = hashlib.sha256(password).hexdigest()
        
            with connection.cursor() as cursor:
                query = "SELECT IFNULL( (SELECT account_id FROM login WHERE login = '"+login+"' AND password = '"+hash_password+"'), 'null' )"
                cursor.execute(query)
                for row in cursor.fetchall():
                    if row[0] == "null":
                        print("Wrong login credentials")
                    else:
                        account_id = row[0]
                
        elif userInput == 2:
            print("Creating account...")
            login = input("login: ")
            password = input("password: ")
            first_name = input("first_name: ")
            last_name = input("last_name: ")
            balance = float(input("balance: "))

            password = bytes(password, "utf-8")
            hash_password = hashlib.sha256(password).hexdigest()
            
            with connection.cursor() as cursor:
                query = "INSERT INTO account(first_name, last_name, balance) VALUES ('"+first_name+"', '"+last_name+"', "+str(balance)+" )"
                cursor.execute(query)

                query = "SELECT LAST_INSERT_ID()"
                cursor.execute(query)
                account_id = cursor.fetchall()[0][0]

                query = "INSERT INTO login(account_id, login, password) VALUES ( "+str(account_id)+", '"+login+"', '"+hash_password+"' )"
                cursor.execute(query)
                
            connection.commit()

        elif userInput == 3:
            break

        if account_id != 0:
            while True:
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Show account details")
                print("4. exit")
                userInput = int(input())

                if userInput == 1:
                    with connection.cursor() as cursor:
                        query = "SELECT balance FROM account WHERE account_id = "+str(account_id)
                        cursor.execute(query)
                        balance = cursor.fetchall()[0][0]
                        print("current balance: ", balance)
                        to_add = input("amount to deposit: ")
                        balance = int(balance) + float(to_add)

                        query = "UPDATE account SET balance = "+str(balance)+" WHERE account_id = "+str(account_id)
                        cursor.execute(query)
                        print("new balance: ", balance)
                        
                    connection.commit()
                
                elif userInput == 2:
                    with connection.cursor() as cursor:
                        query = "SELECT balance FROM account WHERE account_id = "+str(account_id)
                        cursor.execute(query)
                        balance = cursor.fetchall()[0][0]
                        print("current balance: ", balance)
                        to_add = input("amount to withdraw: ")
                        balance = int(balance) - float(to_add)
                        if balance < 0:
                            print("error, amount to withdraw too high")
                            continue

                        query = "UPDATE account SET balance = "+str(balance)+" WHERE account_id = "+str(account_id)
                        cursor.execute(query)
                        print("new balance: ", balance)
                        
                    connection.commit()
                
                elif userInput == 3:
                    with connection.cursor() as cursor:
                        query = "SELECT * FROM account WHERE account_id = "+str(account_id)
                        cursor.execute(query)
                        for row in cursor.fetchall():
                            print(row)
                
                elif userInput == 4:
                    break

finally:
    connection.close()
