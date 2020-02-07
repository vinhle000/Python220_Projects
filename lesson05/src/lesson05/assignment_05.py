import pymongo
import dns # required for connecting with SRV
import getpass

#p = getpass.getpass(prompt="Enter Pass: ", stream=None)
#client = pymongo.MongoClient("mongodb+srv://kay:myRealPassword@cluster0.mongodb.net/test?w=majority")
client = pymongo.MongoClient("mongodb+srv://uwvinh:uwtest2020@cluster0-ksxsk.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
print(db)