#!/usr/bin/python

import pymysql
import datetime

# Open database connection
db = pymysql.connect(host= "127.0.0.1",user="root",password = "root",database= "toll_collection_system")

user_qr_code = "1506"
user_balance = "100"

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO User_Information(QR_Code_Number, \
       Balance) \
       VALUES ('%s', '%s')" % \
       (user_qr_code,user_balance)

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
