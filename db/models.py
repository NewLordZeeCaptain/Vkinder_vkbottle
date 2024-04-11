from peewee import Model, ForeignKeyField, IntegerField, TextField, PostgresqlDatabase


db = PostgresqlDatabase(
    "postgres", user="postgres", host="192.168.31.112", password="postgres"
)


class BaseModel(Model):
    class Meta:
        # database = sqlitedb
        database = db


class User(BaseModel):
    user_id = IntegerField(unique=True)
    first_name = TextField()
    last_name = TextField()
    sex = IntegerField()
    city = IntegerField()
    age = IntegerField()
    status = IntegerField()


class Candidate(BaseModel):
    user = ForeignKeyField(
        User,
        backref="candidates",
        on_delete="CASCADE",
    )
    vk_id = IntegerField(unique=True)
    first_name = TextField()
    last_name = TextField()


class Favorite(BaseModel):
    user = ForeignKeyField(User, backref="favorites", on_delete="CASCADE")
    vk_id = IntegerField(unique=True)
    first_name = TextField()
    last_name = TextField()
    photos = TextField()
    city = IntegerField()


class Blacklist(BaseModel):
    user = ForeignKeyField(User, backref="blacklists", on_delete="CASCADE")
    vk_id = IntegerField(unique=True)
    first_name = TextField()
    last_name = TextField()
