import pymongo

class mongoConnect:
    pass

    def QueryIdlerDmi(url,key):
        uri = f'{url}'
        client = pymongo.MongoClient(uri)
        db=client.polin
        collection = db.get_collection('statuses')
        #cursor = collection.find({'key':f'{key}','idler':{'$exists':True},'latch_status':{'$exists':True}}).limit(1)
        cursor = collection.find({'key':f'{key}'}).sort('timestamp',pymongo.DESCENDING).limit(1)

        for item in cursor: #cursor.sort('timestamp',pymongo.DESCENDING):
            if 'latch_status' not in item:
                item['latch_status'] = None
                latch_status = item['latch_status']
            else:
                latch_status = item['latch_status']

            if 'idler' not in item:
                item['idler'] = 'Sensor sin ubicacion'
                idler = item['idler']
            else:
                idler = item['idler']
            
            return idler, latch_status
        cursor.close()
