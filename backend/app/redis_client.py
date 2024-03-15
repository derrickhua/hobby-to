import redis

class RedisClient:
    def __init__(self, app=None):
        self.client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        redis_url = app.config['REDIS_URL']
        self.client = redis.from_url(redis_url)

    def get(self, name):
        return self.client.get(name)

    def setex(self, name, time, value):
        return self.client.setex(name, time, value)

redis_client = RedisClient()