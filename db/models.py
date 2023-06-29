# from sqlalchemy.ext.declarative import declarative_base
# import sqlalchemy as sq

# Base = declarative_base()
from peewee import *
# db = PostgresqlDatabase()
sqlitedb = SqliteDatabase('developing.db')
db = PostgresqlDatabase('postgres',user='postgres',host='92.51.36.19',password='postgres')

class BaseModel(Model):
    class Meta:
        # database = sqlitedb
        database = db

class User(BaseModel):
    vk_id = IntegerField(unique=True)
    first_name = TextField()
    last_name = TextField()
    sex = IntegerField()

    
class Favorite(BaseModel):
    user_id = ForeignKeyField(User, backref='favorite', on_delete="CASCADE")
    vk_id = IntegerField(unique=True)
    first_name = TextField()
    last_name = TextField()
    photos = TextField()
    city = IntegerField()
    
class Blacklist(BaseModel):
    user_id = ForeignKeyField(User, backref='blacklist',on_delete="CASCADE")
    vk_id = IntegerField(unique=True)
    first_name = TextField()
    last_name = TextField()
    
    

# # Пользователь бота ВК
# class User(Base):
#     __tablename__ = "user"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.Integer, unique=True)


# class Favorite(Base):
#     __tablename__ = "favorite"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     first_name = sq.Column(sq.String)
#     last_name = sq.Column(sq.String)
#     photos = sq.Column(sq.String)
#     vk_id = sq.Column(sq.Integer, unique=True)
#     user_id = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


# class Blacklist(Base):
#     __tablename__ = "blacklist"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.Integer, unique=True)
#     user_id = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


# Анкеты добавленные в избранное
# class DatingUser(Base):
#     __tablename__ = "dating_user"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.Integer, unique=True)
#     first_name = sq.Column(sq.String)
#     second_name = sq.Column(sq.String)
#     city = sq.Column(sq.Integer)
#     link = sq.Column(sq.String)
#     user_id = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


# # Фото избранных анкет
# class Photos(Base):
#     __tablename__ = "photos"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     link_photo = sq.Column(sq.String)
#     count_likes = sq.Column(sq.Integer)
#     id_dating_user = sq.Column(
#         sq.Integer, sq.ForeignKey("dating_user.id", ondelete="CASCADE")
#     )


# # Анкеты в черном списке
# class BlackList(Base):
#     __tablename__ = "black_list"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.Integer, unique=True)
#     first_name = sq.Column(sq.String)
#     second_name = sq.Column(sq.String)
#     city = sq.Column(sq.Integer)
#     link = sq.Column(sq.String)
#     link_photo = sq.Column(sq.String)
#     count_likes = sq.Column(sq.Integer)
#     id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))
