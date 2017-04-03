from mongoengine import *


class FoodItem(Document):
    src = StringField()
    image = FileField()
    title = StringField()
    description = StringField()