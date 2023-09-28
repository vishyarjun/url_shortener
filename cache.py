import redis

class Cache:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get(self, key):
        cached_data = self.redis_client.get(key)
        if cached_data:
            return cached_data.decode('utf-8')
        return None

    def set(self, url, hsh):
        self.redis_client.set(url, hsh)
        self.redis_client.set(hsh, url)

    def remove(self, key):
        value = self.redis_client.get(key)
        
        self.redis_client.delete(key)
        if value:
            self.redis_client.delete(value)
        


