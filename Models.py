from peewee import *

db = SqliteDatabase('data.db')

class Users(Model):
    id = AutoField()
    username = CharField(60, unique=True)
    password = CharField(30)
    email = CharField(60)

    class Meta:
        database = db
        db_table = 'Users'

class Hall(Model):
    id = AutoField()
    row1 = CharField(12)
    row2 = CharField(12)
    row3 = CharField(12)
    row4 = CharField(12)
    row5 = CharField(12)
    row6 = CharField(12)
    row7 = CharField(12)
    row8 = CharField(12)
    row9 = CharField(12)
    row10 = CharField(12)

    class Meta:
        database = db
        db_table = 'Hall'
    


class Performance(Model):
    id = AutoField()
    title = CharField()
    place_config = ForeignKeyField(Hall,backref='hall')

    class Meta:
        database = db
        db_table = 'Performance'

class Book(Model):
    id = AutoField()
    user = ForeignKeyField(Users, backref='users')
    perf = ForeignKeyField(Performance, backref='perf')

    class Meta:
        database = db
        db_table = 'Book'










        
