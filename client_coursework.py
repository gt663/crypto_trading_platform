#######################for importing different libraries ###########################

from socket import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import datetime
import random
import time
from tkinter import ttk

######## class to connect with server##################################################################################
class Connection:
    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 5001
        self.BUFSIZE = 1024
        self.ADDRESS = (self.HOST, self.PORT)
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect(self.ADDRESS)

    #### function to receive mssg #####
    def recver(self):
        # to ensure connection test
        recv = self.s.recv(self.BUFSIZE)
        mssg = recv.decode()
        return mssg

    #### function to send mssg ###########
    def sender(self, option):
        json_string = json.dumps(option)  # Convert the list to a JSON string
        self.s.send(json_string.encode())

    def sen(self, optio):
        option = str(optio)
        self.s.send(option.encode())

    def receive_response(self):
        data = self.s.recv(1024)  # Receive data from the server (up to 1024 bytes)
        response = json.loads(data.decode())  # Convert the JSON data to a Python dictionary
        return response

    #### function to close the connection ####
    def close_connection(self):
        self.s.close()

################ to create a gui for accounts sign in/log in #############################################3######33######
class Accounts_gui:
    def __init__(self):
        self.root = Tk()
        self.root.title('welcome on your investment platform')
        self.root.geometry("1100x700+210+55")
        self.root.config(bg='pink')
        self.value = 0
        self.user_entry = ""
        self.password_entry = ""
        self.cash_entry = ""
        # merging with connection class ###
        self.connection = Connection()
        self.cash_invested = 0

    #### to create the different text labels ###########
    def labels(self, variable1, variable2):
        label_login = Label(self.root, text=variable1, font=("Times New Roman", 35),background='pink')
        label_login.place(x=600, y= 60)
        label_username = Label(self.root, text="username", font=20,background='pink')
        label_username.place(x=750, y=160)
        label_password = Label(self.root, text="password", font=20,background='pink')
        label_password.place(x=750, y=270)
        label_cash = Label(self.root, text="cash to invest", font=20,background='pink')
        label_cash.place(x=750, y=390)
        label_signin = Label(self.root, text=variable2, font=("arial", 10), background='pink')
        label_signin.place(x=733, y=570)

######### entry widgets #################################
    def entry_credentials1(self):
        self.user_entry = Entry(self.root, width=30)
        self.user_entry.place(x=750, y=180)

    def entry_credentials2(self):
        self.password_entry = Entry(self.root, width=30)
        self.password_entry.place(x=750, y=290)

    def entry_credentials3(self):
        self.cash_entry = Entry(self.root, width=30)
        self.cash_entry.place(x=750, y=410)

    ########### to validate credentials and contains function to database ########
    def validity(self):

        #### to retrieve the values ######
        user = self.user_entry.get()
        password = self.password_entry.get()
        cash = self.cash_entry.get()
        login_validate = True

        # to validate a proper acceptable username
        if len(user) < 9 or len(user) > 11:
            label_error1 = Label(self.root, text="*username must contain 10 characters*", fg="red",
                                 font=('arial', 10), bg='pink')
            label_error1.place(x=750, y=210)
            login_validate = False
            self.entry_credentials1()

        ##### to validate username starting with alpha #########
        if len(user) >= 1:
            if user[0].isalpha():
                pass
            else:
                label_error1 = Label(self.root, text="*username must start with an alphabet  *", fg="red",
                                     font=('arial', 10), bg='pink')
                label_error1.place(x=750, y=210)
                login_validate = False
                self.entry_credentials1()

        ###### to validate a proper acceptable password###########
        bolean = True
        if len(password) < 9 or len(password) > 11:
            label_error2 = Label(self.root, text="*password must contain 10 characters*", fg="red",
                                 font=('arial', 10), bg='pink')
            label_error2.place(x=750, y=310)
            login_validate = False
            self.entry_credentials2()
            bolean = False

        ##### to validate a strong password ###############
        if bolean == True:
            alpha = 0
            num = 0
            for i in range(len(password)):
                if password[i].isalpha():
                    alpha += 1
                if password[i].isdigit():
                    num += 1
            if alpha <= 5 or alpha >= 9 or num >= 5 or num <= 1:
                label_error2 = Label(self.root, text="*min 6-8 alphabets and 2-4 numbers  *", fg="red",
                                     font=('arial', 10), bg='pink')
                label_error2.place(x=750, y=310)
                login_validate = False
                self.entry_credentials2()

            ######## to validate a proper acceptable cash input################
            count = 0
            bolean2 = True
            for j in range(len(cash)):
                if cash[j].isdigit():
                    count = count + 1
            if not count == len(cash):
                label_error3 = Label(self.root, text="*please insert the integer values only*         ", fg="red",
                                     font=('arial', 10), bg='pink')
                label_error3.place(x=750, y=430)
                bolean2 = False
                login_validate = False
                self.entry_credentials3()
            ##### to make money greater that 5000 ###############
            if bolean2 == True:
                if not cash:
                    login_validate = False
                    self.entry_credentials3()

                if self.value == 1:
                    if cash < str(5000):
                        label_error3 = Label(self.root, text="*initial investment must be above $5000*", fg="red",
                                             font=('arial', 10), bg='pink')
                        label_error3.place(x=750, y=430)
                        login_validate = False
                        self.entry_credentials3()

        ############ to call another function if credentials are good to log in ##########
            if login_validate == True:
                self.check_agaist_server_database(user, password, cash)


########## to connect to database function is called above in validity #######################
    def check_agaist_server_database(self, user, password, cash):
        while True:
            va = self.value
            var = str(va)
            list = [user, password, var, cash]
            self.connection.sender(list)
            res = self.connection.receive_response()
            print(res)
            client_id =""
            cash_invest_total = ""
            if res != 0 and res != 1:
                respo = res[0]
                response = ''.join([char for char in respo if char.isdigit()])
                ident = res[1]
                client_id = ''.join([char for char in ident if char.isdigit()])
                cas = res[2]
                cash_invest_total = ''.join([char for char in cas if char.isdigit()])
                self.to_otherclasscash(cash_invest_total)
            else:
                if self.value == 0:
                    response = "0"
                else:
                    response = "1"

            if response == '0' and self.value == 0:
                self.error_login()
                break
            if response == '1' and self.value == 0:
                self.login_credential_good(client_id, cash_invest_total)
                break
            if response == '0' and self.value == 1:
                self.signin_credentials_good(client_id, cash_invest_total)
                 #welcome
                break
            if response == '1' and self.value == 1:
                self.error_signin()  #this account already existss
                break

    ####### when sign in is good ##########
    def signin_credentials_good(self, n1, n2):
        self.login_credential_good(n1, n2)

    def to_otherclasscash(self, op):
        self.cash_invested = int(op)

    ###### when sign in is not good ##########
    def error_signin(self):
        messagebox.showwarning("warning", "this account already exists")
        self.entry_credentials1()
        self.entry_credentials2()
        self.entry_credentials3()
    ###### when login is good and sign in is good to go on main page ##########
    def login_credential_good(self, variable, total_invest):
        self.root.destroy()
        self.mainpage = Mainpage(self.cash_invested)
        #self.mainpage.loadbackground()
        self.mainpage.label1(variable, total_invest)
        image1 = "platform_images/atm.png"
        image2 = "platform_images/profile.png"
        image3 = "platform_images/invest.png"
        self.mainpage.add_button(image1)
        self.mainpage.profile_button(image2)
        self.mainpage.invest_button(image3)
        self.mainpage.mainloop()

    #### when login is not good ###########
    def error_login(self):
         messagebox.showwarning("warning", "cant find this account please try again")
         self.entry_credentials1()
         self.entry_credentials2()
         self.entry_credentials3()

    #######asthetics ##########
    def color_left_frame(self):
        left_color = Frame(self.root, width=450, height=20, bg='white')
        left_color.pack(fill=BOTH, side=LEFT)

    ##### on click function ####
    def on_click(self):
        self.validity()

    ####### login button to initiate process ###########
    def login_button(self, variable3):
        button = Button(self.root, text=variable3, bg='navy blue', width=19, fg='white', font=("arial", 10),
                        relief=RAISED, command=self.on_click)
        button.place(x=770, y=470)

    ################# to change window into the signing mode ####
    def signing(self):
        self.value = 1
        variable_text1 = "signin to a new account"
        variable_text2 = "happy your joining us  "
        self.labels(variable_text1, variable_text2)
        variable_text3 = "sign in"
        self.login_button(variable_text3)
        variable_text4 = "The journey starts HERE"
        self.radio_buttons(variable_text4)


     ###### the signing in button ##################
    def signin(self, variable5):
        button = Button(self.root, text=variable5, bg='pink', width=10, font=("arial", 9), relief=RAISED,
                        command=self.signing)
        button.place(x=870, y=568)

################# the design part left of the gui with images ###############################################
    def radio_buttons(self, variable4):
        variable_option = StringVar()
        variable_option.set("1")
        variable_option.trace("w", lambda *args: self.text_picture_left(variable_option, variable4))
        radio1 = Radiobutton(self.root, bg='white',variable=variable_option, value="1")
        radio1.place(x=180, y=660)
        radio2 = Radiobutton(self.root, bg='white',variable=variable_option, value="2")
        radio2.place(x=200, y=660)
        self.text_picture_left(variable_option, variable4)

    ######## loading images and changing when needed also the texts #######################
    def text_picture_left(self, option, variable4):
         text_label = Label(self.root, text="", font=('arial', 20), fg="navy blue")
         text_label.place(x=100, y=140)
         z = option.get()
         ###button 1####
         if z == "1":
             text_label.config(text=variable4)

             # Open the original image
             original_image = Image.open("platform_images/cryto_welcome.gif")

             # Convert and save the image in GIF format (a supported format for PhotoImage)
             original_image.save("platform_images/cryto_welcome.gif", format="GIF")

             photo = PhotoImage(file='platform_images/cryto_welcome.gif')
             lb1 = Label(self.root, image=photo)
             lb1.image = photo
             lb1.place(x=127, y=280)
         ###button 2#########
         if z == "2":
             text_label.config(text="range of crytocurrencies ")

             photo = PhotoImage(file='platform_images/crypto.png')
             lb2 = Label(self.root, image=photo)
             lb2.image = photo
             lb2.place(x=120, y=280)

    #### the end statement ########
    def dogui(self):
        self.root.mainloop()

###################################class for the main page of the platformm ###########################################
class Mainpage:
    def __init__(self, cash_invested):
        self.window = Tk()
        self.window.title('HOME Page')
        self.window.geometry("1200x700+150+55")
        self.window.config(bg="black")
        # merging with connection class
        self.connection = Connection()
        self.cash_invested_total = cash_invested

    def label1(self, variable_id, investment):
        label_welcome = Label(self.window, text="welcome", font=("times new romans", 60, "bold"), width=15, bg="black",fg="white")
        label_welcome.place(x=590, y=540)

        label_id = Label(self.window, text="your ID :", font=("times new romans", 20), bg="black",fg="white")
        label_id.place(x=819, y=500)
        label_id = Label(self.window, text=variable_id, font=("times new romans", 20), bg="black",fg="white")
        label_id.place(x=939, y=500)

        label_invest = Label(self.window, text="withdraw/add", font=("times new romans", 15,"bold"), width=10, bg="black", fg="green")
        label_invest.place(x=80, y=540)

        label_profile = Label(self.window, text="portfolio", font=("times new romans", 15,"bold"), bg="black", fg="green")
        label_profile.place(x=434, y=400)

        label_atm = Label(self.window, text="Invest now", font=("times new romans", 15,"bold"), bg="black", fg='green')
        label_atm.place(x=790, y=250)

        label_invest_value = Label(self.window, text="investment value : ", font=("times new romans", 15, "bold"),
                             bg="black", fg="white")
        label_invest_value.place(x=50, y=40)
        label_invest_value = Label(self.window, text=investment, font=("times new romans", 15, "bold"),
                                   bg="black", fg="white")
        label_invest_value.place(x=260, y=40)

        label_cash_inhand = Label(self.window, text="cash in hand : 500000", font=("times new romans", 15, "bold"),
                             bg="black", fg="white")
        label_cash_inhand.place(x=50, y=80)

        label_toatal_profit = Label(self.window, text="total gain/loss : 50000", font=("times new romans", 15, "bold"),
                             bg="black", fg="white")
        label_toatal_profit.place(x=50, y=120)

    def loadbackground(self):
        # Load the background image
        # Load the original image
        original_image = Image.open("platform_images/graph-crypto.png")

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 1200
        new_height = 700
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image
        lb2 = Label(self.window, image=photo, bd=0)
        lb2.image = photo
        lb2.place(x=0, y=0, relwidth=1, relheight=1)


    def onpress_invest(self):
        self.window.destroy()
        self.invest_page = Invest_page(self.cash_invested_total)
        variable_image1 = "platform_images/etherum.png"
        variable_image2 = "platform_images/bitcoin.png"
        variable_image3 = "platform_images/silver.png"
        self.invest_page.Ethereum_button(variable_image1)
        self.invest_page.bitcoin_button(variable_image2)
        self.invest_page.silver_button(variable_image3)
        priceseth = None
        pricebit = None
        pricesil = None
        self.invest_page.label_coins(pricebit, priceseth, pricesil)
        self.invest_page.update_coins_data()
        self.invest_page.mains()


    def onpress_add(self):
        self.add_take = With_add()
        self.add_take.entery_cash()
        self.add_take.adding_button()
        self.add_take.label_with()


    def onpress_profile(self):
        self.profiling = Portfolio()
        with open("transaction_files/table_port.txt", 'w') as file:
            file.write("1")
        with open("transaction_files/output.txt", 'r') as file:
            data = file.readlines()
        self.profiling.make_table(data)

    def invest_button(self, image_button):
        # Load the original image
        original_image = Image.open(image_button)

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 150
        new_height = 160
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image

        lb4 = Button(self.window, image=photo, bd=0, command=self.onpress_invest)
        lb4.image = photo
        lb4.place(x=760, y=50)

    def profile_button(self, image_button):
        # Load the background image
        # Load the original image
        original_image = Image.open(image_button)

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 150
        new_height = 160
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image
        lb4 = Button(self.window, image=photo, bd=0, command=self.onpress_profile)
        lb4.image = photo
        lb4.place(x=400, y=200)

    def add_button(self, image_button):
        # Load the background image
        # Load the original image
        original_image = Image.open(image_button)

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 150
        new_height = 160
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image
        lb4 = Button(self.window, image=photo, bd=0, command=self.onpress_add)
        lb4.image = photo
        lb4.place(x=65, y=340)

    def mainloop(self):
        self.window.mainloop()

############################################# invest page class ########################################################
class Invest_page:
    def __init__(self, cash):
        self.window_inve = Tk()
        self.window_inve.title('Investment Page')
        self.window_inve.geometry("1300x700+90+55")
        # merging with connection class
        self.window_inve.config(bg="black")
        self.connecting2 = Connection()
        self.background()
        self.total_investment = cash
        self.little_window2 = None
        self.window_buy_sel = None
        self.window_confirm = None
        self.quantity = None
        self.inve = None
        self.option =None
        self.current_date = None
        self.crypto_name =None
        self.price = None
        self.pricebi =None
        self.pricesi =None
        self.priceset = None

    def label_coins(self,price_bit, price_eth, price_sil):
        label_1 = Label(self.window_inve, text="Name: Bitcoin ", font=("times new romans", 13, "bold"), width=15, bg="white")
        label_1.place(x=552, y=390)
        label_1 = Label(self.window_inve, text=f"price: {price_bit}", font=("times new romans", 13, "bold"), width=15, bg="white")
        label_1.place(x=552, y=418)

        label_2 = Label(self.window_inve, text="Nane: Etherum ", font=("times new romans", 13, "bold"), width=15, bg="white")
        label_2.place(x=1022, y=390)
        label_2 = Label(self.window_inve, text=f"price: {price_eth}", font=("times new romans", 13, "bold"), width=15, bg="white")
        label_2.place(x=1022, y=418)

        label_3 = Label(self.window_inve, text="Name: Silver metal ", font=("times new romans", 13, "bold"), width=15, bg="white")
        label_3.place(x=102, y=390)
        label_3 = Label(self.window_inve, text=f"price: {price_sil}", font=("times new romans", 13, "bold"), width=15, bg="white")
        label_3.place(x=102, y=418)
    def edit_button(self):
        self.destroy_confirmation_buttons()
        self.buy_or_sell()

    def cancel_button(self):
        labelmessage = messagebox.askyesno("Question", "cancel transaction?")
        if labelmessage:
            self.destroy_confirmation_buttons()
            self.window_inve.destroy()
            mms = Accounts_gui()
            va = ""
            mms.login_credential_good(va, self.total_investment)

    def confirm_pay_button(self):
        self.destroy_confirmation_buttons()
        self.window_confirm_pay = Toplevel(master=self.window_inve)
        self.window_confirm_pay.geometry("600x400+600+320")
        self.window_confirm_pay.config(bg="grey")
        # Get the current date and time
        current_datetime = datetime.datetime.now()
        # Extract the date from the datetime object
        self.current_date = current_datetime.date()
        label = Label(self.window_confirm_pay, text=f"name of cryptocurrency : {self.crypto_name}", bg='grey', font=("Arial", 17))
        label.place(x=200, y=40)
        label = Label(self.window_confirm_pay, text=f"Date : {self.current_date}", bg='grey', font=("Arial", 17))
        label.place(x=200, y=100)
        label = Label(self.window_confirm_pay, text=f"transaction : {self.option}", bg='grey', font=("Arial", 17))
        label.place(x=200, y=160)
        label = Label(self.window_confirm_pay, text=f"quantity :{self.quantity}", bg='grey', font=("Arial", 17))
        label.place(x=200, y=220)
        label = Label(self.window_confirm_pay, text=f"cost : {self.inve}", bg='grey', font=("Arial", 17))
        label.place(x=200, y=280)
        button_end = Button(self.window_confirm_pay, text="ok", font=("Arial", 17), bg='black'
                            , fg='grey', command=self.destroy_last_window)
        button_end.place(x=270, y=340)
        self.send_buying_transaction()

    def update_coins_data(self):
        # Generate random values for the coins
        w = random.randint(50, 500)
        wi = str(w)
        p = random.randint(50, 800)
        pi = str(p)
        l = random.randint(50, 1000)
        li = str(l)

        # Set the coin prices as class attributes (if needed)
        self.priceset = pi
        self.pricebi = li
        self.pricesi = wi

        # Update the label with the new coin prices
        self.label_coins(self.pricebi, self.priceset, self.pricesi)

        # Schedule the next update after 5 seconds (5000 milliseconds)
        self.window_inve.after(15000, self.update_coins_data)

    def destroy_last_window(self):
        self.window_confirm_pay.destroy()

    def destroy_confirmation_buttons(self):
        self.window_confirm.destroy()

    def confirmation_buy(self):
        self.option = "buy"
        self.window_confirm = Toplevel(master=self.window_inve)
        self.window_confirm.geometry("600x400+600+320")
        self.window_confirm.config(bg="grey")
        label = Label(self.window_confirm, text="confirmation", bg='grey', font=("Arial", 17))
        label.place(x=200, y=70)
        button_buy = Button(self.window_confirm, text="confirm & pay", bg='black', fg='grey',
                            font=("Arial", 17), command=self.confirm_pay_button)
        button_buy.place(x=70, y=200)
        button_buy = Button(self.window_confirm, text="Edit", font=("Arial", 17),bg='black'
                            , fg='grey',command=self.edit_button)
        button_buy.place(x=290, y=200)
        button_buy = Button(self.window_confirm, text="cancel", font=("Arial", 17), bg='black',
                            fg='grey', command=self.cancel_button)
        button_buy.place(x=410, y=200)

    def confirmation_sell(self):
        self.option = "sell"
        self.window_confirm = Toplevel(master=self.window_inve)
        self.window_confirm.geometry("600x400+600+320")
        self.window_confirm.config(bg="grey")
        label = Label(self.window_confirm, text="confirmation", bg='grey', font=("Arial", 17))
        label.place(x=200, y=70)
        button_buy = Button(self.window_confirm, text="confirm & pay", bg='black', fg='grey',
                            font=("Arial", 17), command=self.confirm_pay_button)
        button_buy.place(x=70, y=200)
        button_buy = Button(self.window_confirm, text="Edit", font=("Arial", 17), bg='black'
                            , fg='grey', command=self.edit_button)
        button_buy.place(x=290, y=200)
        button_buy = Button(self.window_confirm, text="cancel", font=("Arial", 17), bg='black',
                            fg='grey', command=self.cancel_button)
        button_buy.place(x=410, y=200)
        self.destroy2()

    def destroy2(self):
        self.window_buy_sell.destroy()

    def buy_or_sell(self):
        self.window_buy_sell = Toplevel(master=self.window_inve)
        self.window_buy_sell.geometry("600x400+600+320")
        self.window_buy_sell.config(bg="grey")
        label_text = Label(self.window_buy_sell, text="Do you want to buy or sell", bg='grey', font=("arial", 15))
        label_text.place(x=170, y=80)
        button_buy = Button(self.window_buy_sell, text="buy", font=("Arial", 17), command=self.onpress_buy)
        button_buy.place(x=200, y=210)
        button_sell = Button(self.window_buy_sell, text="sell", font=("Arial", 17), command=self.onpress_sell)
        button_sell.place(x=350, y=210)

    def invest_if_possible_buy(self, reply1, reply2):

        bool = True
        if reply1 and int(reply1) > 0:
            if reply1.isdigit() == True:
                if int(reply1) <= int(self.total_investment):
                    bool = False
                    repl = int(reply1)
                    self.inve = repl
                    updated_cash_in = int(self.total_investment) - int(self.inve)
                    self.total_investment = int(self.total_investment) - int(self.inve)
                    with open("transaction_files/cash.txt", 'w') as file:
                        updated_cash = str(updated_cash_in)
                        file.write(updated_cash)
                    if self.price == 1:
                        amount = repl / int(self.pricebi)
                    if self.price == 2:
                        amount = repl / int(self.priceset)
                    if self.price == 3:
                        amount = repl / int(self.pricesi)
                    self.quantity = round(amount, 3)
                    self.destroy()
                    self.confirmation_buy()


        if bool == True:
            if reply2 and reply2.isdigit() == True:
                if int(reply2) > 0:
                    repy = int(reply2)
                    if self.price == 1:
                        self.inve = repy * int(self.pricebi)
                    if self.price == 2:
                        self.inve = repy * int(self.priceset)
                    if self.price == 3:
                        self.inve = repy * int(self.pricesi)
                    self.quantity =reply2
                    if int(self.inve) <= int(self.total_investment):
                        updated_cash_in = int(self.total_investment) - int(self.inve)
                        self.total_investment = int(self.total_investment) - int(self.inve)
                        with open("transaction_files/cash.txt", 'w') as file:
                            updated_cash = str(updated_cash_in)
                            file.write(updated_cash)
                        self.destroy()
                        self.confirmation_buy()

    def destroy(self):
        self.little_window.destroy()

    def invest_if_possible_sell(self, reply1, reply2):
        pass
        '''
        bool = True
        if reply1 and int(reply1) > 0:
            if reply1.isdigit() == True:
                if int(reply1) <= int(crypto):
                    bool = False
                    repl = int(reply1)
                    self.inve = repl
                    updated_cash_in = int(self.total_investment) - int(self.inve)
                    self.total_investment = int(self.total_investment) - int(self.inve)
                    with open("transaction_files/cash.txt", 'w') as file:
                        updated_cash = str(updated_cash_in)
                        file.write(updated_cash)
                    if self.price == 1:
                        amount = repl / int(self.pricebi)
                    if self.price == 2:
                        amount = repl / int(self.priceset)
                    if self.price == 3:
                        amount = repl / int(self.pricesi)
                    self.quantity = round(amount, 3)
                    self.destroy()
                    self.confirmation_sell()

        if bool == True:
            if reply2 and reply2.isdigit() == True:
                if int(reply2) > 0:
                    repy = int(reply2)
                    if self.price == 1:
                        self.inve = repy * int(self.pricebi)
                    if self.price == 2:
                        self.inve = repy * int(self.priceset)
                    if self.price == 3:
                        self.inve = repy * int(self.pricesi)
                    self.quantity = reply2
                    if int(self.inve) <= int(self.total_investment):
                        updated_cash_in = int(self.total_investment) - int(self.inve)
                        self.total_investment = int(self.total_investment) - int(self.inve)
                        with open("transaction_files/cash.txt", 'w') as file:
                            updated_cash = str(updated_cash_in)
                            file.write(updated_cash)
                        self.destroy()
                        self.confirmation_sell()
        '''
    def onpress_sell(self):
        self.destroy2()
        self.little_window = Toplevel(master=self.window_inve)
        self.little_window.geometry("600x400+600+320")
        self.little_window.config(bg="grey")
        # Add a label to the little_window
        label_text = Label(self.little_window, text="either Enter the amount of money you ready to invest", bg='grey',
                           font=("arial", 12))
        label_text.place(x=50, y=30)

        # Add an entry widget to the little_window
        entry_input = Entry(self.little_window, font=("Arial", 12))
        entry_input.place(x=50, y=80)

        label_text2 = Label(self.little_window, text=" or Enter the quantity you would like to buy/sell", bg='grey',
                            font=("arial", 12))
        label_text2.place(x=50, y=130)

        entry_input2 = Entry(self.little_window, font=("Arial", 12))
        entry_input2.place(x=50, y=180)

        button_submit = Button(self.little_window, text="submit", font=("Arial", 12),
                               command=lambda: self.invest_if_possible_sell(entry_input.get(), entry_input2.get()))
        button_submit.place(x=60, y=220)

    def onpress_buy(self):
        self.destroy2()
        self.little_window = Toplevel(master=self.window_inve)
        self.little_window.geometry("600x400+600+320")
        self.little_window.config(bg="grey")
        # Add a label to the little_window
        label_text = Label(self.little_window, text="either Enter the amount of money you ready to invest", bg='grey', font=("arial",12))
        label_text.place(x=50, y=30)

        # Add an entry widget to the little_window
        entry_input = Entry(self.little_window, font=("Arial", 12))
        entry_input.place(x=50, y=80)

        label_text2 = Label(self.little_window, text=" or Enter the quantity you would like to buy/sell", bg='grey',
                           font=("arial", 12))
        label_text2.place(x=50, y=130)

        entry_input2 = Entry(self.little_window, font=("Arial", 12))
        entry_input2.place(x=50, y=180)

        button_submit = Button(self.little_window, text="submit", font=("Arial", 12),
                               command=lambda: self.invest_if_possible_buy(entry_input.get(), entry_input2.get()))
        button_submit.place(x=60, y=220)

    def Ethereum_button(self, image_button):
        self.crypto_name = "Etherum"
        self.price = 2
        # Load the original image
        original_image = Image.open(image_button)

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 170
        new_height = 180
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image

        lb4 = Button(self.window_inve, image=photo, bd=0, command=self.named, bg="black")
        lb4.image = photo
        lb4.place(x=1020, y=200)

    def bitcoin_button(self, image_button):
        self.crypto_name = "Bitcoin"
        # Load the original image
        original_image = Image.open(image_button)

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 170
        new_height = 180
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image

        lb4 = Button(self.window_inve, image=photo, bd=0, command=self.name, bg="black")
        lb4.image = photo
        lb4.place(x=552, y=200)

    def silver_button(self, image_button):
        self.crypto_name = "silver"
        # Load the original image
        original_image = Image.open(image_button)

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 170
        new_height = 180
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image

        lb4 = Button(self.window_inve, image=photo, bd=0, command=self.nam, bg="black")
        lb4.image = photo
        lb4.place(x=102, y=200)

    def nam(self):
        self.crypto_name = "Silver"
        self.buy_or_sell()

    def name(self):
        self.crypto_name = "Bitcoin"
        self.buy_or_sell()

    def named(self):
        self.crypto_name = "Etherum"
        self.buy_or_sell()

    def background(self):
        # Load the background image
        # Load the original image
        original_image = Image.open("platform_images/invest_back.png")

        # Resize the image to the desired dimensions (new_width, new_height)
        new_width = 1300
        new_height = 700
        resized_image = original_image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image
        lb2 = Label(self.window_inve, image=photo, bd=0)
        lb2.image = photo
        lb2.place(x=0, y=0, relwidth=1, relheight=1)

    def send_buying_transaction(self):
        o= str(self.quantity)
        a =str(self.inve)
        b =str(self.option)
        c =str(self.current_date)
        d =str(self.crypto_name)
        list_data =[ o, a, b, c, d]
        with open("transaction_files/data_port.txt", 'w') as file:
            file.write('\n'.join(list_data))

    def mains(self):
        self.window_inve.mainloop()

############################################ class for profile ########################################################
class Portfolio:
    def __init__(self):
        self.window_port = Tk()
        self.window_port.title('portfolio Page')
        self.window_port.geometry("1300x700+90+55")
        # merging with connection class
        self.window_port.config(bg="white")
        self.connecting3 = Connection()

    def make_table(self, data):
        text_widget = Text(self.window_port, wrap=NONE)
        text_widget.pack(expand=True, fill="both")

        # Insert the data into the Text widget
        for row in data:
            text_widget.insert("end", row)


############################################ class for money add?take #################################################
class With_add:
    def __init__(self):
        self.window_with = Tk()
        self.window_with.title('cash in/out Page')
        self.window_with.geometry("1000x600+90+55")
        # merging with connection class
        self.window_with.config(bg="pink")
        self.connecting4 = Connection()
        self.entery = None

    def entery_cash(self):
        self.entery = Entry(self.window_with ,font=("arial", 18), width=16, bg="grey", fg="black")
        self.entery.place(x=400, y=300)

    def check_entry(self):
        boolean = False
        check = self.entery.get()
        checks = str(check)
        if checks:
            if checks.isdigit() == True:
                boolean = True
        return boolean

    def onpress_add(self):
        if self.check_entry() ==True:
            check = self.entery.get()
            with open("transaction_files/getting_cash.txt", "w") as file:
                file.write("1")
            with open("transaction_files/cash_retrieve.txt", "r")as fil:
                price = str(fil.read())
                new_price = int(check) + int(price)
                new_prices = str(new_price)
                with open("transaction_files/cash_file.txt", "w") as fil:
                    fil.write("1")
                with open("transaction_files/cash_new_up.txt", "w")as file:
                    file.write(new_prices)


    def onpress_with(self):
        if self.check_entry() == True:
            check = self.entery.get()
            price = 5000
            if check < price:
                new_price = price - check


    def adding_button(self):
        adding = Button(self.window_with, text="add",width=14, font=("bold", 16), command=self.onpress_add)
        adding.place(x=200, y=450)
        take = Button(self.window_with, text="withdraw",width=14, font=("bold", 16), command=self.onpress_with)
        take.place(x=600, y=450)

    def label_with(self):
        label_id = Label(self.window_with, text="withdraw/add", font=("times new romans", 23), bg="pink", fg="black")
        label_id.place(x=390, y=100)

#to test connection with server
'''
hr = Connection()
msssg = hr.recver()
print(msssg)
hr.close_connection()
'''
def main():
    # to test whole gui ########################
    test = Accounts_gui()
    variable_text1 = "login to your account"
    variable_text2 = "don't have an account?"
    test.labels(variable_text1, variable_text2)
    test.entry_credentials1()
    test.entry_credentials2()
    test.entry_credentials3()
    test.color_left_frame()
    variable_text3 = "login"
    test.login_button(variable_text3)
    variable_text5 = "sign in"
    test.signin(variable_text5)
    variable_text4 = "lovely to have you back "
    test.radio_buttons(variable_text4)
    test.dogui()

if __name__ == "__main__":
    main()
