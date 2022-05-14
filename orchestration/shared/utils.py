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
product1 = Product(id="123", name="Chocolate", price=299)
product2 = Product(id="abc", name="Juice", price=799)


def populate_users_data(redis_instance: redis.Redis):
    redis_instance.set(name=user1.card_token, value=json.dumps(user1.reprJSON()))
    redis_instance.set(name=user2.card_token, value=json.dumps(user2.reprJSON()))


def populate_products_data(redis_instance: redis.Redis):
    redis_instance.set(name=product1.id, value=json.dumps(product1.reprJSON()))
    redis_instance.set(name=product2.id, value=json.dumps(product2.reprJSON()))
