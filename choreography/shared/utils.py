import json

import redis
from shared.models import User

user1 = User(card_token="123abc123", name="John", surname="Stones")
user2 = User(card_token="123-123-123", name="Harry", surname="Kane")


def populate_users_data(redis_instance: redis.Redis):
    redis_instance.set(name=user1.card_token, value=json.dumps(user1.reprJSON()))
    redis_instance.set(name=user2.card_token, value=json.dumps(user2.reprJSON()))
