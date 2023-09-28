import pymongo

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://admin:admin@localhost:27017/')
        self.db = self.client['url_shortener']

    def get_hash_from_url(self, url):
        url_hash_doc = self.db.url_hashes.find_one({'url': url})
        if url_hash_doc:
            return url_hash_doc['hash']
        return None
    
    def get_url_from_hash(self, hsh):
        print(hsh)
        url_hash_doc = self.db.url_hashes.find_one({'hash': hsh})
        
        if url_hash_doc:
            return url_hash_doc.get('url',None)
        return None

    def store_url_hash(self, url, url_hash):
        self.db.url_hashes.insert_one({'url': url, 'hash': url_hash})
    
    def remove_url_hash(self, hash):
        print(hash)
        data_to_remove = {"hash": hash}
        self.db.url_hashes.delete_many(data_to_remove)

# Usage example:
# db = Database(uri='mongodb://localhost:27017/', database_name='mydatabase')
# hash = db.get_url_hash('example.com')
# db.store_url_hash('example.com', 'abc123')
