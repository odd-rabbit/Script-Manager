import pymongo


class DatabaseChecker(object):
    def __init__(self):
        self.address = '192.168.3.189'
        self.port = 9999

    def get_db_status(self):
        client = pymongo.MongoClient(self.address, self.port)
        try:
            client.server_info()
        except:
            return False
        else:
            return True
