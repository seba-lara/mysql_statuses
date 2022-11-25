import pymongo
import pprint

class mongoConnect:
    pass

    def QueryIdlerDmi(url,key):
        uri = f'{url}'

        client = pymongo.MongoClient(uri)

        db=client.polin
        
        collection = db.get_collection('statuses')
        
        cursor = collection.find({'key':f'{key}','idler':{'$exists':True}}).limit(1)

        for item in cursor.sort('timestamp',pymongo.ASCENDING):
            
            """if cursor == None:
                print(f'El sensor {key}, no tiene ubicacion.')
            else
                #print(item['idler'])"""
            return item['idler'],item['latch_status']
        #client.close()
        #return item['idler']
        client.close()
        #return item
    
    """for record in cursor:
        if 'idler' not in record:
            pass
        else:
            print(record)
            i= i+1"""
    

#key = 'Test/Correa de prueba/El sector/M1/EC0'
"""urlmongo = "mongodb://si:tisapolines@192.168.1.119:27017/?authSource=polin&authMechanism=SCRAM-SHA-1"
asd = '/wsn1/0013a20041540c88'
clientemongo = mongoConnect()
clientemongo.QueryIdlerDmi(urlmongo,asd)"""
