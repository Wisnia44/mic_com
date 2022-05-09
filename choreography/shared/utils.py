import json

import redis
from shared.models import Product, User

user1 = User(
    card_token="123abc123",
    name="John",
    surname="Stones",
    address="john.stones@email.com",
)
user2 = User(
    card_token="123-123-123",
    name="Harry",
    surname="Kane",
    address="harry.kane@email.com",
)

product1 = Product(name="Chocolate", price=0, quantity=2)
product2 = Product(name="Juice", price=0, quantity=1)


def populate_users_data(redis_instance: redis.Redis):
    redis_instance.set(name=user1.card_token, value=json.dumps(user1.reprJSON()))
    redis_instance.set(name=user2.card_token, value=json.dumps(user2.reprJSON()))


def get_products_json():
    return [product1.reprJSON(), product2.reprJSON()]
