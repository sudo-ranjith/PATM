import pymongo
import urllib

import socket   
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)   
print("Your Computer Name is:"+hostname)   
print("Your Computer IP Address is:"+IPAddr)  

# connect to mongodb and create a database with A2ZDB then create a collection  USERS
myclient = pymongo.MongoClient("mongodb+srv://8344449313:8344449313@cluster0.8rzwx.mongodb.net/A2ZDB?retryWrites=true&w=majority")
# myclient = pymongo.MongoClient("mongodb+srv://sudo_rk:" + urllib.parse.quote_plus("String@123") + "@cluster0.8rzwx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = myclient.test
mydb = myclient["A2ZDB"]
mycol = mydb["USERS"]


try:
    # insert a document into the users collection
    mydict = { "name": "John", "address": "Highway 37" }
    x = mycol.insert_one(mydict)
    print(x.inserted_id)
except Exception as e:
    print(e)


except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)



# connect mongodb for flask app

