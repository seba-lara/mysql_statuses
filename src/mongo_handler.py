import pymongo
import pprint

#class mongoConnect:

def QueryIdlerDmi(key):
    uri = "mongodb://si:tisapolines@192.168.1.119:27017/?authSource=polin&authMechanism=SCRAM-SHA-1"

    client = pymongo.MongoClient(uri)

    db=client.polin
    
    collection = db.get_collection('statuses')
    
    cursor = collection.find({'key':f'{key}','idler':{'$exists':True}}).limit(1)

    for item in cursor.sort('timestamp',pymongo.ASCENDING):
        if cursor == None:
            print('El sensor no tiene ubicacion')
        else:
            return item['idler']
        #return item
    
    """for record in cursor:
        if 'idler' not in record:
            pass
        else:
            print(record)
            i= i+1"""
    

#key = 'Test/Correa de prueba/El sector/M1/EC0'
asd = '/wsn1/0013a20041540c88'
#clientemongo = mongoConnect()
QueryIdlerDmi(asd)
