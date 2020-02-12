import datetime

import mongoengine
from django.db import models


# Create your models here.

class TestModel(mongoengine.Document):
    title = mongoengine.StringField(
        max_length=300,
    )
    idx = mongoengine.StringField(
    )
    docId = mongoengine.StringField(
    )
    text = mongoengine.StringField(
    )
    link = mongoengine.StringField(
        max_length=300
    )
    create_time = mongoengine.DateTimeField(
        default=datetime.datetime.now
    )
    meta = {'collection': 'recipe', 'strict': False}
