################# for import##

from socket import *
import json
import random
import mysql.connector as mysql
################### class to connect to client##########################################################################
class Server:
    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 5001
        self.BUFSIZE = 1024
        self.ADDRESS = (self.HOST, self.PORT)
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(self.ADDRESS)
        self.server_socket.listen(5)
        self.client_socket = None
        self.account_data = Credential()
        self.mssg1 = None
        self.mssg2r = None

        self.checker = None

    def enable_update_folio(self,n1,n2,n3,n4,n5, n6):
        self.account_data.update_portfolio(n1, n2, n3, n4, n5, n6)

    # general acceptance of server #######################
    def accept_client(self):
        (client, address) = self.server_socket.accept()
        print("Accepted connection from:", address)
        self.client_socket = client

    ###### to send mesaage ######################
    def send_message(self, message):
        self.client_socket.send(message.encode())

    def sender(self, option):
        json_string = json.dumps(option)  # Convert the list to a JSON string
        self.client_socket.send(json_string.encode())

    ############## to receive message of credentials ##############################################
    def receive_mssg1(self):
        try:
            # Check if the client socket is still valid
            if self.client_socket:
                message = self.client_socket.recv(self.BUFSIZE)
                json_string = message.decode()
                received_list = json.loads(json_string)
                self.check_mssg1(received_list[0], received_list[1], received_list[2], received_list[3])
            else:
                print("Connection closed by the client.")
                self.close_connection()
        except ConnectionAbortedError:
            print("Connection closed by the client.")
            self.close_connection()

    ############# to check the received message credentials and add functions to database #########################
    def check_mssg1(self, mssg1, mssg2, checker, mssg3):
        x = self.account_data.selecting_username()
        # Perform the comparison
        boolean = True
        memo = "0"
        ###########for when login is good ############################
        for i in range(len(x)):
            if mssg1 in x[i]:  # user_name####
                y = self.account_data.selecting_password()
                if mssg2 in y[i]:
                    boolean = False
                    memo = "1"
                    if checker == "1":
                        self.send_message(memo)
                        break
                    if checker == "0":
                        self.mssg2r = mssg2
                        i = self.check_clientid(mssg1)
                        identity = str(i)
                        self.update_cash_invested(mssg1, mssg3)
                        cas = self.account_data.selecting_cash_invested(mssg1)
                        cash = str(cas)
                        liste = [memo, identity, cash]
                        self.sender(liste)
                        break

        ########## for when login is not good #######
        if boolean == True and checker == "0":
            self.send_message(memo)

        ########### for when u sign in with good############################333
        if boolean == True and checker == "1":
            self.mssg2r = mssg2
            ###### Generate a list of 7 random digits (from 0 to 9)
            random_digits = [str(random.randint(0, 9)) for _ in range(7)]
            # Concatenate the digits to form the random string
            random_string = ''.join(random_digits)
            ########## calling function to sign in in database ####################
            id_when = self.generate_credential(mssg1, mssg2, random_string, mssg3)
            id_when_new = str(id_when)
            cas = self.account_data.selecting_cash_invested(mssg1)
            cash = str(cas)
            listt = [memo, id_when_new, cash]
            self.sender(listt)

    ############## function calling to put credentials into database##################3########
    def generate_credential(self, user, passe, client, cashin):
         signin_new_id = self.account_data.inserting_signin_values(user, passe, client, cashin)
         return signin_new_id

    ###########function to call select clientid ############################
    def check_clientid(self, value_where):
        client_identity = self.account_data.selecting_clientid(value_where)
        return client_identity

    ###########function to update cash invest in database when login #########
    def update_cash_invested(self, user_variable, mmsg3):
        current_cash = self.account_data.selecting_cash_invested(user_variable)
        new_cash = current_cash + int(mmsg3)
        self.account_data.update_cash_in_database(user_variable, new_cash)

    #####closing######################
    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()

    def receive_mssg3(self):
        if self.client_socket:
            message = self.client_socket.recv(self.BUFSIZE)
            return message

    def receive_mssg2(self):
        if self.client_socket:
            try:
                message = self.client_socket.recv(self.BUFSIZE)
                json_string = message.decode()
                received_list = json.loads(json_string)
                print("Received Message 2:")
                print(received_list[0])
                print(received_list[1])
                print(received_list[2])
                print(received_list[3])
                print("kiiis")
            except ConnectionAbortedError:
                print("Connection closed by the client.")

    def retrieve_data_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Ensure there are exactly 5 lines in the file (o, a, b, c, d).
        if len(lines) != 5:
            raise ValueError("Invalid file format. Expected 5 lines in the file.")

        # Extract and store each line in separate variables.
        o = lines[0].strip()
        a = lines[1].strip()
        b = lines[2].strip()
        c = lines[3].strip()
        d = lines[4].strip()

        return o, a, b, c, d

    def is_file_empty(self, file_path):
        with open(file_path, 'r') as file:
            return len(file.read()) == 0

    def empty_file(self, file_path):
        with open(file_path, 'w') as file:
            file.truncate()

    def put_folio_file(self):
        desired_option = "password12"
        select_data_query = "SELECT Quantity, price, `option`, date, crypto_name  FROM datafolio WHERE password = %s "
        # Execute the SELECT query
        self.account_data.cursor.execute(select_data_query, (desired_option,))
        # Fetch all the rows (records) from the result set
        result_set = self.account_data.cursor.fetchall()

        # Close the cursor after fetching the data
        self.account_data.cursor.close()

        # Process the fetched data if needed (optional)
        # For example, you can format the data, convert it to a specific format, etc.

        # Write the data into a file
        output_file = "transaction_files/output.txt"
        with open(output_file, "w") as file:
            for row in result_set:
                # Assuming each row contains strings or numbers, you can join the values and write them as a comma-separated line
                line = ",".join(str(value) for value in row)
                file.write(line + "\n")

    def getting_cash_update_buy(self, cash):
        desired_option = self.mssg2r
        update_query = "UPDATE accounts SET cash_invest = %s WHERE password = %s"
        desired_optio = self.mssg2r# Replace this with the actual user name you want to update
        data_to_update = (cash, desired_optio)
        self.account_data.cursor.execute(update_query, data_to_update)
        self.account_data.db.commit()


############################################## class credentials #######################################################
class Credential:
    def __init__(self):
        self.db = mysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database="credentials"
        )
        self.cursor = self.db.cursor()

    ###################### selecting cash invested #####################
    def selecting_cash_invested(self, user_variable):
        # Execute the SELECT query to fetch data from the database
        query = "SELECT cash_invest FROM accounts WHERE user_name = %s"
        self.cursor.execute(query, (user_variable,))
        # Fetch all the values from the query result
        database_value = self.cursor.fetchone()
        return int(database_value[0])

    def selecting_cash_invest(self, pass_variable):
        # Execute the SELECT query to fetch data from the database
        query = "SELECT cash_invest FROM accounts WHERE password = %s"
        self.cursor.execute(query, (pass_variable,))
        # Fetch all the values from the query result
        database_value = self.cursor.fetchone()
        return int(database_value[0])

    ########################## selecting username ####################
    def selecting_username(self):
        # Execute the SELECT query to fetch data from the database
        query = "SELECT user_name FROM accounts"
        self.cursor.execute(query)
        # Fetch all the values from the query result
        database_values = [row[0] for row in self.cursor.fetchall()]
        return database_values

    #########################selecting clientid ######################
    def selecting_clientid(self, variable):
        # Execute the SELECT query to fetch data from the database
        query = "SELECT clientid FROM accounts WHERE user_name = %s"
        self.cursor.execute(query, (variable,))
        # Fetch all the values from the query result
        database_values = [row[0] for row in self.cursor.fetchall()]
        return database_values

    ########################## selecting password ###################
    def selecting_password(self):
        # Execute the SELECT query to fetch data from the database
        query = "SELECT password FROM accounts "
        self.cursor.execute(query)
        # Fetch all the values from the query result
        database_value = [row[0] for row in self.cursor.fetchall()]
        return database_value

    ################to updated cash invested in database ##########################
    def update_cash_in_database(self, user, cash):
        # Execute the UPDATE query to update the cash_invest value in the database
        update_query = "UPDATE accounts SET cash_invest = %s WHERE user_name = %s"
        data_to_update = (cash, user)
        self.cursor.execute(update_query, data_to_update)
        self.db.commit()

    def update_cash_database(self, cash, password):
        # Execute the UPDATE query to update the cash_invest value in the database
        update_query = "UPDATE accounts SET cash_invest = %s WHERE password = %s"
        data_to_update = (cash, password)
        self.cursor.execute(update_query, data_to_update)
        self.db.commit()

    ##################### inserting the sign in values into database#############################################
    def inserting_signin_values(self, q, r, u, t):
        # Define the INSERT statement
        insert_query = "INSERT INTO accounts (user_name, password, clientid, cash_invest) VALUES (%s, %s, %s, %s)"

        # Prepare the values to insert
        data_to_insert = (q, r, u, t)

        # Execute the INSERT statement
        self.cursor.execute(insert_query, data_to_insert)

        # Commit the changes to the database
        self.db.commit()
        signin_new = self.selecting_clientid(q)
        return signin_new

    def update_portfolio(self, q, p, o, d, c, f):

        insert_data_query = """
        INSERT INTO datafolio (Quantity, price, `option`, date, crypto_name, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        data_values = (q, p, o, d, c, f)
        self.cursor.execute(insert_data_query, data_values)
        self.db.commit()

    ##closing##############
    def closing(self):
        self.db.close()
        self.cursor.close()

# Testing for connection with the client###############################################################################
server = Server()
w = Credential
print("Waiting for a client to connect...")
server.accept_client()
if True:
    server.receive_mssg1()
    while True:
        #server.receive_mssg2()
        file_path = "transaction_files/data_port.txt"
        if server.is_file_empty(file_path) == False:
            o, a, b, c, d = server.retrieve_data_from_file("transaction_files/data_port.txt")
            # Now, the variables o, a, b, c, and d contain the values retrieved from the file.

            e = server.mssg2r
            server.enable_update_folio(o, a, b, c, d, e)
            server.empty_file(file_path)

        file_path2 ="transaction_files/table_port.txt"
        if server.is_file_empty(file_path2) == False:
            server.put_folio_file()
            server.empty_file(file_path2)

        file_path3 = "transaction_files/cash.txt"
        if server.is_file_empty(file_path3) == False:
            with open("transaction_files/cash.txt","r")as file:
                dat = file.read()
                server.getting_cash_update_buy(dat)
            server.empty_file(file_path3)

        file_path4="transaction_files/getting_cash.txt"
        if server.is_file_empty(file_path4) == False:
            with open("transaction_files/cash_retrieve.txt", "w")as file:
                t = server.mssg2r
                retrieve = server.account_data.selecting_cash_invest(t)
                ret = str(retrieve)
                file.write(ret)
                server.empty_file(file_path4)

        file_path5 = "transaction_files/cash_file.txt"
        if server.is_file_empty(file_path5) == False:
            with open("transaction_files/cash_new_up.txt", "r") as file:
                new = file.read()
                ne = str(new)
                print(ne)
                c = server.mssg2r
                server.account_data.update_cash_database(ne, c)
                server.empty_file(file_path5)




