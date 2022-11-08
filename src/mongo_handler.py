from pymongo import MongoClient
client = MongoClient('10.75.10.166',27017,username='si',password='tisapolines',authSource='polin',authMechanism='SCRAM-SHA-1')

print(client)