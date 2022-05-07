from pydantic import BaseModel


class Card(BaseModel):
    card_token: str

    def reprJSON(self):
        return dict(card_token=self.card_token)


class User(BaseModel):
    card_token: str
    name: str
    surname: str

    def reprJSON(self):
        return dict(card_token=self.card_token, name=self.name, surname=self.surname)

    def dict_init(self, input_dict: dict):
        for key, value in input_dict.items():
            setattr(self, key, value)
