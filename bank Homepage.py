'''
Created on Mar 6, 2018

@author: Admin
'''
import Tkinter as tk  #header or imported modules
import tkMessageBox              
import tkFont as tkFont
import cx_Oracle
import datetime
import os
from prettytable import PrettyTable
   
def showerror():
    tkMessageBox.showerror("Error", "Check your input details")
    
'''To get date at any where'''
def datestore(): 
    present=datetime.datetime.now()
    #print(present)
    t=datetime.datetime.strftime(present, "%d-%m-%Y")    
    #print(t)
    return t

def datestring(present): 
    #print(present)
    t=datetime.datetime.strftime(present, "%d-%m-%Y")    
    #print(t)
    return t

def transaction(id,transaction_type,amount,balance): #To store transactions done by anybody anywhere
    con=cx_Oracle.connect("ak/ak25@localhost/xe")
    cur=con.cursor()
    entrydate=datetime.datetime.today()
    
    ''' Table 2: ak_transactionall table to store all transactions happening
    cur.execute("CREATE TABLE ak_transactionall(accountno int, dates Date, transaction_type varchar(10),amount float(10),balance float(10) DEFAULT 0)")
    '''
    cur.execute("INSERT INTO ak_transactionall VALUES(:1,:2,:3,:4,:5)",{'1':id,'2':entrydate,'3':transaction_type,'4':amount,'5':balance})
    con.commit()
    con.close()
    return

def destroy(): #to destroy the main window
    container.quit()
    
def logoutuser(): #to signout user from the account
    tkMessageBox.showinfo("Logout","Successfully Logged Out")
    app.show_frame("home")

def logoutadmin(): #to signout admin from the account
    tkMessageBox.showinfo("Admin Logout","Successfully Logged Out")
    app.show_frame("home")
    
def display_print(statements):
        bgcolor= '#87CEEB'
        printer=tk.Tk()
        printer.title("Records")
        T=tk.Text(printer,height=20,width=100)
        T.pack()
        T.insert(tk.END, statements)
        printer.mainloop()
     
class App(tk.Tk):  # main frame 
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, "Global Bank")
        tk.Tk.geometry(self, "520x450")
        self.title_font = tkFont.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.title_font1 = tkFont.Font(family='Helvetica', size=18, weight="bold")
        self.title_font2= tkFont.Font(family='Times New Roman', size=12)
        self.title_font3= tkFont.Font(family='Times New Roman', size=10)
        global container
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.winfo_rgb('#FF8C69')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        global parent,controller
        for F in (home,option1,option2,option3,subdivisions,addresschange, \
                  moneydeposit,moneywithdrawal,printstatement,moneytransfer,accountclosure,logout,subdivisions3,closedaccounts):  
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("home")
        
    def show_frame(self, page_name): #to change the frames
        frame = self.frames[page_name]
        frame.tkraise()
 
        
class home(tk.Frame): # main screen
    def move_screen(self):
        #print(choice)
        if(choice==4):
            destroy()
        else:
            app.show_frame(choosen)
        
    def __init__(self, parent, controller):
        bgcolor='#EECBAD'#'#5F9EA0'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Global Bank", font=controller.title_font,bg='#F0FFF0',fg='#5F9EA0')
        label.pack(side="top", fill="x", pady=10)
        texts="""Welcome to Global Bank Services 
        If You are new to our services, Please select "SignUp" option to register   
        If You are already registered, Please select "SignIn" to get out services      """
        label = tk.Label(self, text=texts, font=controller.title_font2,bg=bgcolor)
        label.pack(side="top", fill="x", pady=10)
        label = tk.Label(self, text="-------------------------------------------------------------------", font=controller.title_font1,bg=bgcolor)
        label.pack(side="top", fill="x", pady=0)
        label = tk.Label(self, text="Main Menu", font=controller.title_font1,bg=bgcolor)
        label.pack(side="top", fill="x", pady=10)  
        try:      
            global v
            v=tk.IntVar()
            tk.Radiobutton(self,text="SignUp (New Customer)",font=controller.title_font2,bg=bgcolor,variable=v,value=1,command=self.sel).pack()
            tk.Radiobutton(self,text="SignIn (Old Customer)    ",font=controller.title_font2,bg=bgcolor,variable=v,value=2,command=self.sel).pack()
            tk.Radiobutton(self,text="Admin SignUp                ",font=controller.title_font2,bg=bgcolor,variable=v,value=3,command=self.sel).pack()
            tk.Radiobutton(self,text="Quit                                ",font=controller.title_font2,bg=bgcolor,variable=v,value=4,command=self.sel).pack()     
            label = tk.Label(self, text="", font=controller.title_font,bg=bgcolor)
            label.pack(side="top", fill="x", pady=0)
            button1 = tk.Button(self,font=controller.title_font2, bg='#F5F5F5',text="Confirm",command=self.move_screen)
            button1.pack()  
        except:
            showerror()
        
    def sel(self):  #to select the respective options
        global choice,choosen
        try:
            choice = v.get() 
            #print(choice)
            if(choice==1):
                choosen='option1'
            elif(choice==2):
                choosen='option2'
            elif(choice==3):
                choosen='option3'
            else:
                choosen='option4'
            #print(choosen)
        except:
            showerror()
                   
class option1(tk.Frame): #Option1 - signup for new customers
    
    '''To check the password length'''
    def checkpass(self):
        if(password.isalnum()!=True):
                    tkMessageBox.showinfo("Password Error","Plz enter valid input(only Alphabets and numbers)")
                    return 1
                
        if(len(password)<8):
                    tkMessageBox.showinfo("Change your Password","length should be atleast 8 characters")
                    return 1    
        return 0
    
    '''To check the password and confirm_password are same'''
    def checkconfirmpassword(self):
        if(password==confirm_password):
            return 0
        else:
            tkMessageBox.showinfo("Check your passwords","Passwords are not same")
            return 1

    '''To check the pincode'''
    def checkpincode(self):
        if(pincode.isdigit()!=True):
            tkMessageBox.showerror("Pincode Error","pincode should be numeric digits only")
            return 1
        
        if(len(pincode)!=6):
            tkMessageBox.showerror("Pincode Error","pincode should be 6 numeric digits")
            return 1
        return 0
    
    '''minimum balance check'''
    def minbalance(self):
        if(acc_type=='Current Account'):
            if(amount<5000):
                tkMessageBox.showerror("Minimum Balance","The minimum balance must be 5000/- for your account type")
                return 1
        
        if(acc_type=='Savings Account'):
            if(amount<0):
                tkMessageBox.showerror("Minimum Balance","The minimum balance must be 0/- for your account type")
                return 1    
        return 0 
    
    '''Saving the received details into database'''
    def savingdetails(self):
        customerid_begin=700002
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        cur.execute("SELECT * FROM ak_bankdatabase")
        cur.fetchall()
        rows=cur.rowcount
        #print(rows)
        customerid=rows+customerid_begin
        global id
        id=customerid
        
        ''' Table 1: ak_bankdatabase to store all information about customer along with id.
            cur.execute("CREATE TABLE ak_bankdatabase (customerid int PRIMARY KEY, firstname varchar(20),lastname varchar(20), line1 varchar(50),\
                     line2 varchar(50),city varchar(20),state varchar(20),pincode int,country varchar(20), password varchar(20), account_type varchar(20),\
                      balance float(10),user_type varchar(10),locking int,attempt int,transactions int DEFAULT 0)")'''
        
        cur.execute("INSERT INTO ak_bankdatabase VALUES(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,'customer',0,3,1)",\
                    {'1':customerid,'2':f_name,'3':l_name,'4':line1,'5':line2,'6':city,'7':state,\
                     '8':pincode,'9':country,'10':password,'11':acc_type,'12':amount})
        transaction(customerid,'Credit',amount,amount)
        con.commit()
        con.close()
        return
    
    '''Registration form'''
    def register(self):  
        try:
            global f_name,l_name,line1,line2,city,state,pincode,password,confirm_password,acc_type,amount,country 
            f_name=opt1_e1.get()
            l_name=opt1_e2.get()
            line1=opt1_e3.get()
            line2=opt1_e4.get()
            city=opt1_e5.get()
            state=opt1_e6.get()
            country=opt1_e7.get()
            pincode=opt1_e8.get()
            if(self.checkpincode()):
                return
            password=opt1_e9.get()
            confirm_password=e10.get()
            if(self.checkpass()):
                return
            if(self.checkconfirmpassword()):
                return
            acc_type=acc.get()
            amount=float(e11.get())
            if(self.minbalance()):
                return
        except:
            showerror()
        #print(f_name,l_name)
        #print(acc_type)
        self.savingdetails()
        tkMessageBox.showinfo("Registered","signing up successfully.Your account number and customerid is "+str(id))
        opt1_e1.delete(0,tk.END)
        opt1_e2.delete(0,tk.END)
        opt1_e3.delete(0,tk.END)
        opt1_e4.delete(0,tk.END)
        opt1_e5.delete(0,tk.END)
        opt1_e6.delete(0,tk.END)
        opt1_e7.delete(0,tk.END)
        opt1_e8.delete(0,tk.END)
        opt1_e9.delete(0,tk.END)
        e10.delete(0,tk.END)
        e11.delete(0,tk.END)
        return

    def __init__(self, parent, controller):
        bgcolor='#FFFAFA'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Registration Form", font=controller.title_font1,fg='#8B008B',bg=bgcolor)
        label.grid(row=0,columnspan=3)
        label = tk.Label(self,bg=bgcolor, text="------------------------------------------------------------------------------------------------------------------------")
        label.grid(row=1,columnspan=4)
        button = tk.Button(self, text="back",
                           command=lambda: controller.show_frame("home"))
        button.grid(row=18,column=1,sticky='W')
        
        global opt1_e1,opt1_e2,opt1_e3,opt1_e4,opt1_e5,opt1_e6,opt1_e7,opt1_e8,opt1_e9,e10,e11
        tk.Label(self,font=controller.title_font2, text="First Name",bg=bgcolor).grid(row=2,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Last Name ",bg=bgcolor).grid(row=3,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Address   ",bg=bgcolor, fg='#4682B4').grid(row=4,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Line 1    ",bg=bgcolor).grid(row=5,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Line 2    ",bg=bgcolor).grid(row=6,sticky='W')
        tk.Label(self,font=controller.title_font2, text="City      ",bg=bgcolor).grid(row=7,sticky='W')
        tk.Label(self,font=controller.title_font2, text="State     ",bg=bgcolor).grid(row=8,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Country   ",bg=bgcolor).grid(row=9,sticky='W')
        tk.Label(self,font=controller.title_font2, text='Pincode    ',bg=bgcolor).grid(row=10,sticky='W')
        label = tk.Label(self, text="Pincode must be 6 digit",bg=bgcolor, font=controller.title_font3)
        label.grid(row=10,column=2,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Password  ",bg=bgcolor).grid(row=11,sticky='W')
        label = tk.Label(self, text="length should be min 8 characters",bg=bgcolor, font=controller.title_font3)
        label.grid(row=11,column=2,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Confirm Password",bg=bgcolor).grid(row=12,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Account type",bg=bgcolor).grid(row=13,sticky='W')
        tk.Label(self,font=controller.title_font2, text="Amount Deposit",bg=bgcolor).grid(row=14,sticky='W')   
              
        opt1_e1=tk.Entry(self,bg='#E0FFFF')
        opt1_e1.grid(row=2,column=1,sticky='W')
        opt1_e1.focus_set()
        opt1_e2 = tk.Entry(self,bg='#E0FFFF')
        opt1_e2.grid(row=3, column=1,sticky='W')
        opt1_e2.focus_set()
        opt1_e3 = tk.Entry(self,bg='#E0FFFF')
        opt1_e3.grid(row=5,column=1,sticky='W')
        opt1_e3.focus_set()
        opt1_e4 = tk.Entry(self,bg='#E0FFFF')
        opt1_e4.grid(row=6,column=1,sticky='W')
        opt1_e4.focus_set()
        opt1_e5 = tk.Entry(self,bg='#E0FFFF')
        opt1_e5.grid(row=7,column=1,sticky='W')
        opt1_e5.focus_set()
        opt1_e6 = tk.Entry(self,bg='#E0FFFF')
        opt1_e6.grid(row=8,column=1,sticky='W')
        opt1_e6.focus_set()
        opt1_e7 = tk.Entry(self,bg='#E0FFFF')
        opt1_e7.grid(row=9,column=1,sticky='W')
        opt1_e7.focus_set()
        opt1_e8 = tk.Entry(self,bg='#E0FFFF')
        opt1_e8.grid(row=10,column=1,sticky='W')
        opt1_e8.focus_set()
        opt1_e9 = tk.Entry(self,bg='#E0FFFF')
        opt1_e9.grid(row=11,column=1,sticky='W')
        opt1_e9.focus_set()
        e10 = tk.Entry(self,bg='#E0FFFF')
        e10.grid(row=12,column=1,sticky='W')
        e10.focus_set() 
        global acc
        acc=tk.StringVar()
        tk.Radiobutton(self, text="Savings Account",bg=bgcolor,variable=acc, value="Savings Account").grid(row=13,column=1,sticky='W')
        tk.Radiobutton(self, text="Current Account",bg=bgcolor,variable=acc, value="Current Account").grid(row=13,column=2,sticky='W')
        e11 = tk.Entry(self,bg='#E0FFFF')
        e11.grid(row=14,column=1,sticky='W')
        e11.focus_set()         
        tk.Label(self, text=" ",bg=bgcolor).grid(row=15,sticky='E')      
        b2=tk.Button(self,text="Register",command=self.register).grid(row=18,column=0,sticky='E')


class option2(tk.Frame): #Option2 - Sigining in for exisiting customers
    def check(self):
        try:
            global username,user_password
            username=int(opt2_e1.get())
            user_password=opt2_e2.get()
            #print(username,user_password)  
        except:
            showerror()    
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        
        '''Checking user exist'''
        cur.execute("SELECT customerid FROM ak_bankdatabase")
        all_user=cur.fetchall()
        #print(all_user)
        customerlist=[]
        user_exist=0
        for x in range(len(all_user)):
            customerlist.append(all_user[x][0])
            if(username==customerlist[x]):
                user_exist=1
        #print(customerlist)       
        if(user_exist==0):
            tkMessageBox.showinfo("User Not Found","Check Your customerid and password. if new, Register YourDetails and create new bank account") 
            return      
        
        '''checking the account is lock or not'''
        cur.execute("SELECT locking FROM ak_bankdatabase WHERE customerid =:1",{'1':username})
        lockposition=cur.fetchone()
        #print(lockposition)
        lockvalue=lockposition[0]
        #print(lockvalue)
        if(lockvalue==1):
            tkMessageBox.showinfo("Account Locked","Your Account is locked plz contact bank")
            opt2_e1.delete(0,tk.END)
            opt2_e2.delete(0,tk.END)
            return 
        else:
            cur.execute("SELECT attempt FROM ak_bankdatabase WHERE customerid =:1",{'1':username})
            attempt=cur.fetchone()
            #print(attempt)
            attem=attempt[0]
            global success
            success=0
            if(attem>0):
                if(self.check_database(attem)):
                    global name
                    cur.execute("SELECT firstname FROM ak_bankdatabase WHERE customerid =:1",{'1':username})
                    name=cur.fetchone()
                    #print(name)
                    tkMessageBox.showinfo("Login Successful","Welcome "+name[0])
                    success=1
                    #next subdivision
                else:
                    opt2_e2.delete(0,tk.END)
                    attem=attem-1
                    cur.execute("""UPDATE ak_bankdatabase
                                    SET attempt=:2
                                    WHERE customerid =:1""",{'1':username,'2':attem})
                    con.commit()
                    if(attem>0):
                        return
                
            if(success==1):
                cur.execute("""UPDATE ak_bankdatabase
                                SET attempt=:2,locking=:3
                                WHERE customerid =:1""",{'1':username,'2':3,'3':0})
                con.commit()
                global id
                id=username
                opt2_e1.delete(0,tk.END)
                opt2_e2.delete(0,tk.END)
                app.show_frame("subdivisions")
                return 
                
            else:
                tkMessageBox.showinfo("Account Locked","Your Account is locked plz contact bank")
                cur.execute("""UPDATE ak_bankdatabase
                                SET attempt=:2,locking=:3
                                WHERE customerid =:1""",{'1':username,'2':3,'3':1})
                cur.execute("INSERT INTO ak_closedaccounts VALUES(:1,:2)",{'1':username,'2':datestring(datetime.datetime.today())})
                con.commit()
                opt2_e1.delete(0,tk.END)
                opt2_e2.delete(0,tk.END)
                return 
        
    def check_database(self,attem):
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        
        '''password verification'''        
        cur.execute("SELECT password FROM ak_bankdatabase WHERE customerid =:2",{'2':username})
        database_password = cur.fetchone()
        #print(database_password[0])
        #print(user_password)
        if(user_password==database_password[0]):
            return 1
        else:
            tkMessageBox.showinfo("Attempts","Password incorrect. Remaining attempts is "+str(attem-1))
            return  
        
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Customer Login",fg='#00008B',bg=bgcolor, font=controller.title_font1)
        label.grid(row=0,columnspan=2)
        label = tk.Label(self, text="                                                                         ",bg=bgcolor, font=controller.title_font1)
        label.grid(row=1,columnspan=3)
        button = tk.Button(self, text="Cancel",
                           command=lambda: controller.show_frame("home"))
        button.grid(row=6,column=1,sticky='W')
        tk.Label(self,text='Customer Id',bg=bgcolor).grid(row=3,sticky='E')
        tk.Label(self,text='Password    ',bg=bgcolor).grid(row=4,sticky='E')
        
        global opt2_e1,opt2_e2
        opt2_e1=tk.Entry(self)
        opt2_e1.grid(row=3,column=1,sticky='W')
        opt2_e1.focus_set()
        
        opt2_e2=tk.Entry(self,show='*')
        opt2_e2.grid(row=4,column=1,sticky='W')
        opt2_e2.focus_set()
        label = tk.Label(self, text=" ",bg=bgcolor, font=controller.title_font1).grid(row=5)
        b1=tk.Button(self,text="Login",command=self.check).grid(row=6,sticky='E')


class subdivisions(tk.Frame): #Option2 Subdivisions
    def view_profile(self):
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        cur.execute("SELECT * FROM ak_bankdatabase WHERE customerid=:1",{'1':id})
        statements=cur.fetchall()
        t = PrettyTable()
        col1=["Personal Details"," "]
        for x in range(0,len(statements)):
            tup=statements[x]
            #print(tup)
        t.add_column(col1[0],['Name', 'Account Number','Address Line1','Address Line2','City','State','Pincode','Country','Account Type','Balance'])
        t.add_column(col1[1],[tup[1]+tup[2],str(tup[0]),tup[3],tup[4],tup[5],tup[6],tup[7],tup[8],tup[10],tup[11]])
            #print(t) 
        states=t
        display_print(states)
        con.close()
    
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Welcome Customer", font=controller.title_font1,bg=bgcolor)
        label.pack(side="top", fill="x", pady=10)
        
        button1 = tk.Button(self, text="  Address Change     ",
                            command=lambda: controller.show_frame("addresschange"))
        button2 = tk.Button(self, text="    Money Deposit     ",
                            command=lambda: controller.show_frame("moneydeposit"))
        button3 = tk.Button(self, text=" Money Withdrawal ",
                            command=lambda: controller.show_frame("moneywithdrawal"))
        button4 = tk.Button(self, text="   Print Statement     ",
                            command=lambda: controller.show_frame("printstatement"))
        button5 = tk.Button(self, text="     Money Transfer   ",
                            command=lambda: controller.show_frame("moneytransfer"))
        button6 = tk.Button(self, text="   Account Closure   ",
                            command=lambda: controller.show_frame("accountclosure"))
        button7 = tk.Button(self, text="   Customer logout   ",
                            command=logoutuser)
        button8 = tk.Button(self, text="        View Profile       ",
                            command=self.view_profile)
        button1.pack(anchor='w')
        button8.pack(anchor='e')
        button2.pack(anchor='w')
        button3.pack(anchor='e')
        button4.pack(anchor='w')
        button5.pack(anchor='e')
        button6.pack(anchor='w')
        button7.pack(anchor='e')


class addresschange(tk.Frame): #To change the address

    def address(self):
        try:
            new_line1=e1.get()
            new_line2=e2.get()
        except:
            showerror()        
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        cur.execute("""UPDATE ak_bankdatabase
                SET line1=:2, line2=:3
                WHERE customerid =:1""",{'1':id,'2':new_line1,'3':new_line2})
        con.commit()
        e1.delete(0,tk.END)
        e2.delete(0,tk.END)
        tkMessageBox.showinfo("Address Changed", "Your New Address is updated successfully")
        
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Address Change", font=controller.title_font,bg=bgcolor)
        label.grid(row=0,columnspan=3)
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=1,columnspan=2)
        button = tk.Button(self, text="back",
                           command=lambda: controller.show_frame("subdivisions"))
        button.grid(row=6,column=1,sticky='W')   
        
        tk.Label(self,text='Enter Your New Address', font=controller.title_font2,bg=bgcolor).grid(row=2,columnspan=2)
        tk.Label(self,text='Line 1', font=controller.title_font2,bg=bgcolor).grid(row=3)
        tk.Label(self,text='Line 2', font=controller.title_font2,bg=bgcolor).grid(row=4)
        global e1,e2
        e1=tk.Entry(self)
        e1.grid(row=3,column=1)
        e1.focus_set()
        e2=tk.Entry(self)
        e2.grid(row=4,column=1)
        e2.focus_set()
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=5,columnspan=2)
        button2 = tk.Button(self, text="Confirm",command=self.address)
        button2.grid(row=6,column=0,sticky='E')
        
class moneydeposit(tk.Frame):#to deposit money
    def deposit(self):
        try:
            acc_no=int(e3.get())
            new_amount=e4.get()
        except:
            showerror()
        #print(new_amount)
        if(acc_no!=id):
            tkMessageBox.showerror("Error","Account number is not matching..")
            return    
        try:
            con=cx_Oracle.connect("ak/ak25@localhost/xe")
            cur=con.cursor()
            cur.execute("SELECT balance FROM ak_bankdatabase WHERE customerid=:1",{'1':id})
            balancedd=cur.fetchone()
            balanced=balancedd[0]
            #print(balanced)
            #print(float(new_amount))
            balance=balanced+float(new_amount)
            transaction(id,'Credit',new_amount,balance)
            
            #print(balance)
            cur.execute("""UPDATE ak_bankdatabase
                SET balance=:2
                WHERE customerid =:1""",{'1':id,'2':balance})
            con.commit()
            con.close()
            tkMessageBox.showinfo("Money Deposited", """Your Money is deposited successfully.
            The remaining balance in your account is """+str(balance))
            e3.delete(0,tk.END)
            e4.delete(0,tk.END)
        except:
            tkMessageBox.showerror("Money Deposit", "Please Enter Valid Input")
                   
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Money Deposit", font=controller.title_font,bg=bgcolor)
        label.grid(row=0,columnspan=2)
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=1,columnspan=2)
        button = tk.Button(self, text="back",
                           command=lambda: controller.show_frame("subdivisions"))
        button.grid(row=5,column=1,sticky='W') 
        tk.Label(self,text="Enter your account number",bg=bgcolor).grid(row=2,column=0)
        tk.Label(self,text="Enter the amount to deposit",bg=bgcolor).grid(row=3,column=0)
        global e3,e4
        e3=tk.Entry(self)
        e3.grid(row=2,column=1)
        e3.focus_set()
        e4=tk.Entry(self)
        e4.grid(row=3,column=1)
        e4.focus_set()
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=4,columnspan=2)
        button2 = tk.Button(self, text="Confirm",command=self.deposit)
        button2.grid(row=5,column=0,sticky='E')

class moneywithdrawal(tk.Frame): #to withdrawal of money
    def withdraw(self):
        try:
            acc_no=int(e8.get())
            new_amount=e5.get()
        except:
            showerror()
        if(acc_no!=id):
            tkMessageBox.showerror("Error","Account number is not matching..")
            return    
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        cur.execute("SELECT balance FROM ak_bankdatabase WHERE customerid=:1",{'1':id})
        balancedd=cur.fetchone()
        balance=float(balancedd[0])
        #print(balance)
        try:
            balance=balance-float(new_amount)
            #print(balance)
            #print(new_amount)
            cur.execute("SELECT account_type FROM ak_bankdatabase WHERE customerid=:1",{'1':id})
            account=cur.fetchone()
            #print(account)
            if((account[0]=="Savings Account" and balance>=0) or (account[0]=='Current Account' and balance>=5000)):
                cur.execute("""UPDATE ak_bankdatabase
                    SET balance=:2
                    WHERE customerid =:1""",{'1':id,'2':balance})
                transaction(id,'Debit',new_amount,balance)
                con.commit()
                tkMessageBox.showinfo("Money withdrawal", """Your Money withdrawal successfully.
                The Remaining balance in your account is """+str(balance))
                e8.delete(0,tk.END)
                e5.delete(0,tk.END)
            else:
                tkMessageBox.showwarning("Not Possible","You should maintain minimum balance in your account")
                e8.delete(0,tk.END)
                e5.delete(0,tk.END)
        except:
            tkMessageBox.showerror("Money Deposit", "Please Enter Valid Input")
            
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Money Withdrawal", font=controller.title_font,bg=bgcolor)
        label.grid(row=0,columnspan=2)
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=1,columnspan=2)
        button = tk.Button(self, text="back",
                           command=lambda: controller.show_frame("subdivisions"))
        button.grid(row=7,column=1,sticky='W') 
        tk.Label(self,text="Enter Your Account Number",bg=bgcolor).grid(row=4)
        tk.Label(self,text="Enter the amount to Withdraw",bg=bgcolor).grid(row=5)
        global e5,e8
        e8=tk.Entry(self)
        e8.grid(row=4,column=1)
        e8.focus_set()
        e5=tk.Entry(self)
        e5.grid(row=5,column=1)
        e5.focus_set()
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=6,columnspan=2)
        button2 = tk.Button(self, text="Confirm",command=self.withdraw)
        button2.grid(row=7,column=0,sticky='E')  

class printstatement(tk.Frame): #to print statements
    '''To display Transactions'''
    def display(self):
        try:
            global darefrom,dateTo
            datefrom=date1.get()
            dateto=date2.get()

        except:
            showerror()
            
        start=datetime.datetime.strptime(datefrom,"%d-%m-%Y")
        end=datetime.datetime.strptime(dateto,"%d-%m-%Y")
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        if (start < end):
            cur.execute("SELECT * FROM ak_transactionall WHERE accountno=:1 AND dates>=:2 and dates <=:3",{'1':id,'2':start,'3':end})
            statements=cur.fetchall()
        else:
            showerror()
        #print(statements)
        date1.delete(0,tk.END)
        date2.delete(0,tk.END)
        
        t = PrettyTable(['Account Number', 'Date','Transaction Type','Amount','Balance'])
        for x in range(0,len(statements)):
            tup=statements[x]
            #print(tup)
            t.add_row([str(tup[0]),datestring(tup[1]),tup[2],str(tup[3]),str(tup[4])])
        #print(t) 
        states=t
        display_print(states)
        con.close()
        return 
    
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Print Statement", font=controller.title_font,bg=bgcolor)
        label.grid(row=0,columnspan=3)
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=1,columnspan=3)
        global date1,date2
        tk.Label(self,text="Starting date to print",bg=bgcolor).grid(row=3,column=1)
        tk.Label(self,text="(dd/mm/yyyy)",bg=bgcolor).grid(row=3,column=3)
        date1=tk.Entry(self)
        date1.grid(row=3,column=2)
        date1.focus_set()
        tk.Label(self,text="End date to print",bg=bgcolor).grid(row=4,column=1)
        tk.Label(self,text="(dd/mm/yyyy)",bg=bgcolor).grid(row=4,column=3)
        date2=tk.Entry(self)
        date2.grid(row=4,column=2)
        date2.focus_set()
        button = tk.Button(self, text="back",
                           command=lambda: controller.show_frame("subdivisions"))
        button2 = tk.Button(self, text="Print",command=self.display)
        button2.grid(row=5,column=1,sticky='E')
        button.grid(row=5,column=2,sticky='W')
        
       
class moneytransfer(tk.Frame): #To transfer money
    
    def transfer(self):
        receiver_id=e7.get()
        amount_send=e6.get()
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        cur.execute("SELECT balance FROM ak_bankdatabase WHERE customerid=:1",{'1':id})
        balance1=cur.fetchone()
        cur.execute("SELECT balance FROM ak_bankdatabase WHERE customerid=:1",{'1':receiver_id})
        balance2=cur.fetchone()
        balance_sender=balance1[0]
        balance_receiver=balance2[0]
        try:
            balance_sender=balance_sender-float(amount_send)
            balance_receiver=balance_receiver + float(amount_send)
            #print(balance)
            #print(new_amount)
            cur.execute("SELECT account_type FROM ak_bankdatabase WHERE customerid=:1",{'1':id})
            account=cur.fetchone()
            #print(account)
            if((account[0]=="Savings Account" and balance_sender>=0) or (account[0]=='Current Account' and balance_sender>=5000)):
                cur.execute("""UPDATE ak_bankdatabase
                    SET balance=:2
                    WHERE customerid =:1""",{'1':id,'2':balance_sender})
                transaction(id,'Debit',amount_send,balance_sender)
                cur.execute("""UPDATE ak_bankdatabase
                    SET balance=:2
                    WHERE customerid =:1""",{'1':receiver_id,'2':balance_receiver})
                transaction(receiver_id,'Credit',amount_send,balance_receiver)
                con.commit()
                tkMessageBox.showinfo("Money Transfer", """Money Transferred successfully.
                The Available balance in your account is """+str(balance_sender))
                e7.delete(0,tk.END)
                e6.delete(0,tk.END)
            else:
                tkMessageBox.showwarning("Not Possible","You should maintain minimum balance in your account")
                e7.delete(0,tk.END)
                e6.delete(0,tk.END)
        except:
            tkMessageBox.showerror("Money Transfer", "Please Enter Valid Input")
    
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Money Transfer", font=controller.title_font,bg=bgcolor)
        label.grid(row=0,columnspan=2)
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=1,columnspan=2)
        button = tk.Button(self, text="back",
                           command=lambda: controller.show_frame("subdivisions"))
        button.grid(row=5,column=1,sticky='W')
        tk.Label(self,text="Enter the Receiver Account Number   ",bg=bgcolor).grid(row=2)
        tk.Label(self,text="Enter the amount to be transfer",bg=bgcolor).grid(row=3)
        global e7,e6
        e7=tk.Entry(self)
        e7.grid(row=2,column=1)
        e7.focus_set()
        e6=tk.Entry(self)
        e6.grid(row=3,column=1)
        e6.focus_set()
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=4,columnspan=2)
        button2 = tk.Button(self, text="Confirm",command=self.transfer)
        button2.grid(row=5,sticky='E')
        
class accountclosure(tk.Frame): #to delete your account
    
    def close(self):
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        cur.execute("""UPDATE ak_bankdatabase
                    SET locking=:2
                    WHERE customerid =:1""",{'1':id,'2':1})
        
        '''Table 3: ak_closedaccounts to store all the closed accounts with date.
        cur.execute("CREATE TABLE ak_closedaccounts(account int,dates varchar(10))")'''
        
        cur.execute("INSERT INTO ak_closedaccounts VALUES(:1,:2)",{'1':id,'2':datestore()})
        con.commit()
        con.close()
        tkMessageBox.showinfo("Feedback", "Thanks for using our services")
        logoutuser()
        
    def __init__(self, parent, controller):
        bgcolor= '#87CEEB'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Account Closure", font=controller.title_font,bg=bgcolor)
        label.grid(row=0,columnspan=2)
        button = tk.Button(self, text="cancel",
                           command=lambda: controller.show_frame("subdivisions"))
        button.grid(row=3,column=1,sticky='W')
        warning="""Do you want to close your accounts?
                    You can't perform deposit/withdraws and any kind of transactions hereafter.
                    If the conditions are Ok, then click close button or cancel"""
        tk.Label(self,text=warning,bg=bgcolor).grid(row=2,columnspan=2)
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.grid(row=1,columnspan=2)
        button1=tk.Button(self, text="Close",command=self.close)
        button1.grid(row=3,column=0,sticky='E')
    
class logout(tk.Frame): # logout customer

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Customer Logout", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="yes",
                           command=logoutuser)
        button.pack()
        button2 = tk.Button(self, text="cancel",
                           command=lambda: controller.show_frame("subdivisions"))
        button2.pack()
 
class option3(tk.Frame):  #Option3 - Admin Signin  
    def check(self):
        global username,user_password
        try:
            username=int(opt3_e1.get())
            user_password=opt3_e2.get()
            #print(username,user_password)    
        except:
            showerror()
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        
        '''Checking admin exist'''
        cur.execute("SELECT customerid FROM ak_bankdatabase WHERE user_type='admin'")
        all_user=cur.fetchall()
        #print(all_user)
        customerlist=[]
        user_exist=0
        for x in range(len(all_user)):
            customerlist.append(all_user[x][0])
            if(username==customerlist[x]):
                user_exist=1
        #print(customerlist)       
        if(user_exist==0):
            tkMessageBox.showinfo("Admin Not Found","Invalid Admin Id and Password.") 
            return  
                
        global name
        cur.execute("SELECT firstname FROM ak_bankdatabase WHERE customerid=:1",{'1':username})
        got=cur.fetchone()
        name=got[0]
        #print(name)
        cur.execute("SELECT attempt FROM ak_bankdatabase WHERE customerid =:1",{'1':username})
        attempt=cur.fetchone()
        #print(attempt)
        global attem
        attem=attempt[0]
        success=0
        if(attem>0):
            if(self.check_database()):
                tkMessageBox.showinfo("Login Successful","Welcome "+name)
                success=1
            else:
                attem=attem-1
                opt3_e2.delete(0,tk.END)
                cur.execute("""UPDATE ak_bankdatabase
                                    SET attempt=:2
                                    WHERE customerid =:1""",{'1':username,'2':attem})
                con.commit()
                if(attem>0):
                    return
                
        if(success==1):
            cur.execute("""UPDATE ak_bankdatabase
                                SET attempt=:2,locking=:3
                                WHERE customerid =:1""",{'1':username,'2':3,'3':0})
            con.commit()
            opt3_e1.delete(0,tk.END)
            opt3_e2.delete(0,tk.END)
            app.show_frame("subdivisions3")
        else:
            tkMessageBox.showinfo("Attmepts over","Try again later")
            destroy()
            cur.execute("""UPDATE ak_bankdatabase
                                SET attempt=:2,locking=:3
                                WHERE customerid =:1""",{'1':username,'2':3,'3':1})
            con.commit()
            opt3_e1.delete(0,tk.END)
            opt3_e2.delete(0,tk.END)
            return
        return
        
    def check_database(self):
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        '''password verification'''        
        cur.execute("SELECT password FROM ak_bankdatabase WHERE customerid =:2",{'2':username})
        database_password = cur.fetchone()
        #print(database_password[0])
        #print(user_password)
        if(user_password==database_password[0]):
            return 1
        else:
            tkMessageBox.showinfo("Attempts ","Password incorrect. Remaining attempts "+str(attem-1))
            return 
    
    def __init__(self, parent, controller):
        bgcolor='#F5DEB3'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Admin Login In",bg=bgcolor, font=controller.title_font1)
        label.grid(row=0,columnspan=2)
        label = tk.Label(self, text="                                                                         ",bg=bgcolor, font=controller.title_font1)
        label.grid(row=1,columnspan=3)
        button = tk.Button(self, text="Cancel",
                           command=lambda: controller.show_frame("home"))
        button.grid(row=5,column=1,sticky='W')
        tk.Label(self,text='Admin Id',bg=bgcolor).grid(row=2,sticky='E')
        tk.Label(self,text='Password',bg=bgcolor).grid(row=3,sticky='E')
        global opt3_e1,opt3_e2
        
        opt3_e1=tk.Entry(self)
        opt3_e1.grid(row=2,column=1,sticky='W')
        opt3_e1.focus_set()
        
        opt3_e2=tk.Entry(self,show='*')
        opt3_e2.grid(row=3,column=1,sticky='W')
        opt3_e2.focus_set()
        label = tk.Label(self, text="                                                                         ",bg=bgcolor, font=controller.title_font1)
        label.grid(row=4,columnspan=3)
        b1=tk.Button(self,text="login",command=self.check)
        b1.grid(row=5,column=0,sticky='E')   


class subdivisions3(tk.Frame): #Subdivision for Option3
        
    def __init__(self, parent, controller):
        bgcolor='#F5DEB3'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Welcome Admin", font=controller.title_font,bg=bgcolor)
        label.pack()
        label = tk.Label(self, text=" ", font=controller.title_font,bg=bgcolor)
        label.pack()
        
        button1 = tk.Button(self, text="Closed Accounts",
                            command=lambda: controller.show_frame("closedaccounts"))
        button2 = tk.Button(self, text="         Logout        ",command=logoutadmin)
        
        button1.pack()
        button2.pack()
           
class closedaccounts(tk.Frame): #to show cloaed account with exact date
    def accounts(self):
        con=cx_Oracle.connect("ak/ak25@localhost/xe")
        cur=con.cursor()
        cur.execute("SELECT * FROM ak_closedaccounts")
        all_account=cur.fetchall() 
        #print(all_account)
        t = PrettyTable(['Account Number', 'Date'])
        for x in range(0,len(all_account)):
            tup=all_account[x]
            #print(tup)
            t.add_row([str(tup[0]),tup[1]])
        #print(t)
        states=t 
        display_print(states)
        
    def __init__(self, parent, controller):
        bgcolor='#F5DEB3'
        tk.Frame.__init__(self, parent,bg=bgcolor)
        self.controller = controller
        label = tk.Label(self, text="Closed Accounts",bg=bgcolor, font=controller.title_font)
        label.pack()
        label = tk.Label(self, text=" ",bg=bgcolor, font=controller.title_font)
        label.pack()
        button1 = tk.Button(self, text="Show all the Closed Acounts",
                           command=self.accounts)
        button1.pack()
        button = tk.Button(self, text="back",
                           command=lambda: controller.show_frame("subdivisions3"))
        button.pack()
             
if __name__ == "__main__":
    global app
    app = App()
    app.mainloop()