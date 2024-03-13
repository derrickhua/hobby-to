import redis

class RedisClient:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        redis_url = app.config['REDIS_URL']
        self.client = redis.from_url(redis_url)

# Creating a global instance of RedisClient
redis_client = RedisClient()
