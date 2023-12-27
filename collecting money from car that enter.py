from cv2 import *
import time
import cv2
import MySQLdb
import serial
s = serial.Serial('COM1',9600)

current_user =""
localhost = "127.0.0.1"
# Open database connection
db = MySQLdb.connect(localhost,"root","root","toll_collection_system" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
sql_read_database_commad = "select * from User_Information"

# initialize the camera
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that
cam_port = 1
cam = cv2.VideoCapture(cam_port)

# Name of the QR Code Image file
filename = "QR_Image.png"

while(1):
    # reading the input using the camera
    result, image = cam.read()    
    cv2.imwrite("QR_Image.png", image)
    # read the QRCODE image
    image = cv2.imread(filename)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    # detect and decode
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    # if there is a QR code
    # print the data
    if vertices_array is not None:
        #print("QR code number")
        #print(data)
        try:
           # Execute the SQL command
           cursor.execute(sql_read_database_commad)
           # Fetch all the rows in a list of lists.
           results = cursor.fetchall()
           for row in results:
              user_id = row[0]
              user_QR_Code = row[1]
              user_Balance = row[2]
              # Now print fetched result
              #print(user_id)
              #print(user_QR_Code)
              #print(user_Balance)
              if((user_QR_Code == data) and (current_user != user_QR_Code)):
                  print("user ID =" + user_QR_Code)
                  print("ammount delect")
                  time.sleep(1)
                  current_user = user_QR_Code
                  if(int(user_Balance) > 0):
                      s.write(b'1')
                      user_Balance =  str(int(user_Balance) - 10)
                      #print("remaining balance"+user_Balance)
                      sql = """UPDATE User_Information SET Balance = """ + user_Balance + """ WHERE QR_Code_Number = """ + user_QR_Code
                      cursor.execute(sql)
                      db.commit()
                  else:
                      s.write(b'0')
                      print(" Low Balance :: Please recharage ")
                      time.sleep(1)
        except:
            print( "Error: unable to fecth data")
    else:
      print("Reading QR Code.....")
      
# disconnect from server
db.close()
