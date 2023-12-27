#!/usr/bin/python

import MySQLdb
localhost = "127.0.0.1"
# Open database connection
db = MySQLdb.connect(localhost,"root","root","toll_collection_system" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS User_Information")

# Create table as per requirement

sql = """CREATE TABLE User_Information (
         ID int AUTO_INCREMENT PRIMARY KEY,
         QR_Code_Number  CHAR(20) NOT NULL,
	 Balance  CHAR(20) NOT NULL)"""       
cursor.execute(sql)

# disconnect from server
db.close()
