'''
Created on May 10, 2018

@author: Admin
'''

import cx_Oracle


con=cx_Oracle.connect("ak/ak25@localhost/xe")
cur=con.cursor()
cur.execute("CREATE TABLE ak_bankdatabase (customerid int PRIMARY KEY, firstname varchar(20),lastname varchar(20), line1 varchar(50),\
                     line2 varchar(50),city varchar(20),state varchar(20),pincode int,country varchar(20), password varchar(20), account_type varchar(20),\
                      balance float(10),user_type varchar(10),locking int,attempt int,transactions int DEFAULT 0)")
#admin accounts
#cur.execute("INSERT INTO ak_bankdatabase VALUES(600000,'Kumaran','King','Peerkangaranai','Perungalathur','Chennai','Tamil Nadu',600063,'India','arunkumar','Savings Account',5000000.0,'admin',0,3,1)")
#cur.execute("INSERT INTO ak_bankdatabase VALUES(600001,'Kumaran','King','Peerkangaranai','Perungalathur','Chennai','Tamil Nadu',600063,'India','arunkumar','Savings Account',5000000.0,'admin',0,3,1)")

cur.execute("CREATE TABLE ak_transactionall(accountno int, dates Date, transaction_type varchar(10),amount float(10),balance float(10) DEFAULT 0)")

cur.execute("CREATE TABLE ak_closedaccounts(account int,dates varchar(10))")

print("program runned")
con.commit()
con.close()