import pymongo
import urllib

import socket   
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)   
print("Your Computer Name is:"+hostname)   
print("Your Computer IP Address is:"+IPAddr)  

# connect to mongodb and create a database with A2ZDB then create a collection  USERS
myclient = pymongo.MongoClient("mongodb+srv://8344449313:8344449313@cluster0.8rzwx.mongodb.net/patm?retryWrites=true&w=majority")
# myclient = pymongo.MongoClient("mongodb+srv://sudo_rk:" + urllib.parse.quote_plus("String@123") + "@cluster0.8rzwx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = myclient.test
mydb = myclient["patm"]
mycol = mydb["img_db"]


try:
    # insert a document into the users collection
    mydict = {'image': 'medical_bill01.jpg', "labels": [{'id': '1', 'name': 'vendor_address', 'xMin': '286', 'xMax': '841', 'yMin': '110', 'yMax': '141'}, {'id': '2', 'name': 'vendor_name', 'xMin': '492', 'xMax': '811', 'yMin': '41', 'yMax': '82'}, {'id': '3', 'name': 'vendor_dl_no', 'xMin': '328', 'xMax': '566', 'yMin': '141', 'yMax': '171'}, {'id': '4', 'name': 'vendor_gst_no', 'xMin': '562', 'xMax': '818', 'yMin': '142', 'yMax': '171'}, {'id': '5', 'name': 'raw_customer_name_and_code', 'xMin': '51', 'xMax': '568', 'yMin': '166', 'yMax': '202'}, {'id': '6', 'name': 'bill_no', 'xMin': '940', 'xMax': '1196', 'yMin': '169', 'yMax': '199'}, {'id': '7', 'name': 'bill_date', 'xMin': '940', 'xMax': '1156', 'yMin': '196', 'yMax': '223'}, {'id': '8', 'name': 'doctor_name', 'xMin': '50', 'xMax': '477', 'yMin': '196', 'yMax': '225'}, {'id': '9', 'name': 'raw_description', 'xMin': '51', 'xMax': '1252', 'yMin': '222', 'yMax': '640'}, {'id': '10', 'name': 'total_amount', 'xMin': '894', 'xMax': '1252', 'yMin': '643', 'yMax': '688'}, {'id': '11', 'name': 'net_amount', 'xMin': '893', 'xMax': '1255', 'yMin': '749', 'yMax': '791'}, {'id': '12', 'name': 'working_hours', 'xMin': '80', 'xMax': '482', 'yMin': '799', 'yMax': '834'}, {'id': '13', 'name': 'sales_rep_code', 'xMin': '570', 'xMax': '794', 'yMin': '659', 'yMax': '699'}]}
    x = mycol.insert_one(mydict)
    print(x.inserted_id)
except Exception as e:
    print(e)


except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)



# connect mongodb for flask app

