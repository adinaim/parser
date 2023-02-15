from peewee import *
from settings import settings

db = PostgresqlDatabase(settings.db)

class Appartment(Model):
    image = CharField(max_length=200)
    created_at = CharField(max_length=20, null=True)
    currency = CharField(max_length=10, null=True)

    class Meta:
        database = db