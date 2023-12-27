#!/usr/bin/python
import MySQLdb
localhost = "127.0.0.1"

# Open database connection
db = MySQLdb.connect(localhost,"root","root","toll_collection_system" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql = "select * from User_Information"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      user_id = row[0]
      user_QR_Code = row[1]
      user_Balance = row[2]
      # Now print fetched result
      print(user_id)
      print(user_QR_Code)
      print(user_Balance)
      
except:
   print( "Error: unable to fecth data")

# disconnect from server
db.close()




