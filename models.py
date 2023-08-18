from peewee import Model, CharField, ForeignKeyField, SqliteDatabase

db = SqliteDatabase('contacts.db')

class users(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db

class contacts(Model):
    user = ForeignKeyField(users, backref='contacts')
    name = CharField()
    email = CharField(default='')
    phone = CharField(default='')

    class Meta:
        database = db

def create_tables():
    db.create_tables([users, contacts],safe=True)

db.connect()
create_tables()

