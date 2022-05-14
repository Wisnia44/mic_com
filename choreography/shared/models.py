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
    id: str
    name: str
    price: int

    def reprJSON(self):
        return dict(id=self.id, name=self.name, price=self.price)


class ProductId(BaseModel):
    id: str

    def reprJSON(self):
        return dict(id=self.id)
