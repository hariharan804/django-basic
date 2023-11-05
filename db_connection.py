import pymongo

url = 'mongodb+srv://hariharan:<pass>@cluster0.7wkpyye.mongodb.net/'
databaseName = 'user_db'

client = pymongo.MongoClient(url)

try:
    client.admin.command('ping')
    print("You successfully connected to MongoDB!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
except Exception as e:
    print(e)

db = client[databaseName]
