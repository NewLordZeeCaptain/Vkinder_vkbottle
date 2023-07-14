# from configs.config import CONSTR
from db.models import *

# Connecting DB
db.connect()
db.drop_tables([User, Favorite, Blacklist])
db.create_tables([User, Favorite, Blacklist])
# Check if tables exist before dropping and recreating them


# def reg_user(user_id: int):
#     return User.create(vk_id=user_id)


def reg_user(
    vk_id: int, first_name: str, last_name: str, sex: int, city: int, age: int
):
    user = User.create(
        vk_id=vk_id,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        city=city,
        age=age,
    )
    return user


def get_user_info_db(user_id):
    return User.select().where(User.vk_id == user_id).get()


def get_fav(user_id: int):
    return Favorite.select().join(User).where(User.vk_id == user_id).get()


def get_black(user_id: int):
    return Blacklist.select().join(User).where(User.vk_id == user_id).get()


def add_to_favorite(
    user_id: int, vk_id: int, first_name: str, last_name: str, city: int, photos: str
):
    fav = Favorite.create(
        vk_id=vk_id,
        first_name=first_name,
        last_name=last_name,
        city=city,
        photos=photos,
    ).where(User.vk_id == user_id)
    return fav


def add_to_blacklist(user_id: int, vk_id: int, first_name: str, last_name: str):
    black = Blacklist.create(
        vk_id=vk_id, first_name=first_name, last_name=last_name
    ).where(User.vk_id == user_id)
    return black


def remove_from_fav(user_id: int, vk_id: int):
    return Favorite.delete(vk_id=vk_id).where(User.vk_id == user_id)


def remove_from_black(user_id: int, vk_id: int):
    return Blacklist.delete(vk_id=vk_id).where(User.vk_id == user_id)
