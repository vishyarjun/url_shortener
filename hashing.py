import hashlib
import time
import base64
import random
from database import Database
from cache import Cache

class URLHash:
    def __init__(self):
        self.cache = Cache()
        self.db = Database()

    def remove_hash_db_cache(self,hsh):
        self.cache.remove(hsh)
        self.db.remove_url_hash(hsh)
        


    def set_hash_db_cache(self,url,url_hash):
        self.db.store_url_hash(url, url_hash)
        self.cache.set(url, url_hash)
    

    def generate_new_hash(self,url):
        seed = f'{int(time.time()*1000)}_{random.randint(0,1000)}'
        encode = f'{url}{seed}'.encode('utf-8')
        hashobj = hashlib.sha256()
        hashobj.update(encode)
        hash_digest = hashobj.digest()
        new_hash = base64.urlsafe_b64encode(hash_digest).decode('utf-8')[:7]
        return new_hash

    def generate_hash(self, url:str) -> str:
        base64_encoded = self.cache.get(url)
        if base64_encoded:
            return base64_encoded

        base64_encoded = self.db.get_hash_from_url(url)
        if base64_encoded:
            return base64_encoded
        
        
        while base64_encoded is None or self.db.get_url_from_hash(base64_encoded):
            base64_encoded = self.generate_new_hash(url)
        
        self.set_hash_db_cache(url,base64_encoded)

        return base64_encoded
    
    def get_url_from_hash(self,hsh:str)->str:
        url = self.cache.get(hsh)
        if url:
            return url

        url = self.db.get_url_from_hash(hsh)
        
        if url:
            self.cache.set(hsh, url)
            return url
        return None

