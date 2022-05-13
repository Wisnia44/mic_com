from pydantic import BaseModel


class Card(BaseModel):
    card_token: str

    def reprJSON(self):
        return dict(card_token=self.card_token)


class User(BaseModel):
    card_token: str
    name: str
    surname: str
    address: str

    def reprJSON(self):
        return dict(
            card_token=self.card_token,
            name=self.name,
            surname=self.surname,
            address=self.address,
        )


class Product(BaseModel):
    name: str
    price: int
    quantity: int

    def reprJSON(self):
        return dict(name=self.name, price=self.price, quantity=self.quantity)
