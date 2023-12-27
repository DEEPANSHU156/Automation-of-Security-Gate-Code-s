import cv2
import time
import MySQLdb
import serial

# Initialize the serial connection
s = serial.Serial('COM1', 9600)

current_user = ""
localhost = "127.0.0.1"

# Open database connection
db = MySQLdb.connect(
    host=localhost,
    user="root",
    passwd="root",
    db="toll_collection_system"
)

# Prepare a cursor object using cursor() method
cursor = db.cursor()
sql_read_database_commad = "select * from User_Information"

# Initialize the camera
# If you have multiple cameras connected to the current device, assign a value to cam_port
# variable according to that
cam_port = 0  # Change to the correct camera index if needed
cam = cv2.VideoCapture(cam_port)

# Name of the QR Code Image file
filename = "QR_Image.png"

while True:
    # Read the input using the camera
    result, image = cam.read()
    cv2.imwrite("QR_Image.png", image)  # Save the captured frame as "QR_Image.png"

    # Read the QRCODE image
    image = cv2.imread(filename)

    # Initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

    # If there is a QR code
    if vertices_array is not None:
        try:
            # Execute the SQL command
            cursor.execute(sql_read_database_commad)
            
            # Fetch all the rows in a list of lists
            results = cursor.fetchall()

            for row in results:
                user_id = row[0]
                user_QR_Code = row[1]
                user_Balance = row[2]

                if (user_QR_Code == data) and (current_user != user_QR_Code):
                    print("User ID =", user_QR_Code)
                    print("Amount deducted")
                    time.sleep(1)
                    current_user = user_QR_Code

                    if int(user_Balance) > 0:
                        s.write(b'1')
                        user_Balance = str(int(user_Balance) - 10)

                        # Update the user's balance in the database
                        sql = """UPDATE User_Information SET Balance = '""" + user_Balance + """' WHERE QR_Code_Number = '""" + user_QR_Code + """'"""
                        cursor.execute(sql)
                        db.commit()
                    else:
                        s.write(b'0')
                        print("Low Balance :: Please recharge")
                        time.sleep(1)
        except MySQLdb.Error as e:
            print("MySQL Error:", e)
    else:
        print("Reading QR Code...")

# Disconnect from the server
db.close()