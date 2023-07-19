
from db.models import *

# Connecting DB
db.connect()
db.drop_tables([User, Favorite, Blacklist, Candidate])
db.create_tables([User, Favorite, Blacklist, Candidate])



def update_city(user_id, city):
    user = User.get(User.user_id == user_id)
    user.city = city
    user.save()


def update_age(user_id, age):
    user = User.get(User.user_id == user_id)
    user.age = age
    user.save()


def update_status(user_id, status):
    user = User.get(User.user_id == user_id)
    user.status = status
    user.save()


def create_candidate_list(user_id: int, candidate_list: list):
    print("Filtering Candidates\n")
    filtered_candidates = [
        candidate
        for candidate in candidate_list
        if candidate is not None and not candidate.is_closed
    ]
    print("Init DB \n")
    candidates = [
        Candidate.create(
            user=user_id,
            first_name=candidate.first_name,
            last_name=candidate.last_name,
            vk_id=candidate.id,
        )
        for candidate in filtered_candidates
    ]
    return candidates


def get_candidate(user_id):
    max_vk_id = (
        Candidate.select(fn.MAX(Candidate.vk_id))
        .where(Candidate.user_id == user_id)
        .scalar()
    )
    next_vk_id = max_vk_id + 1 if max_vk_id is not None else 1
    return next_vk_id


def clear_candidate_list(user_id):
    Candidate.delete().where(Candidate.user_id == user_id)


def reg_user(
    user_id: int,
    first_name: str,
    last_name: str,
    sex: int,
    city: int,
    age: int,
    status: int,
):
    user = User.create(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        city=city,
        age=age,
        status=status,
    )
    return user


def get_user_info_db(user_id):
    return User.select().where(User.user_id == user_id).get()


def get_fav(user_id: int):
    return Favorite.select().join(User).where(User.vk_id == user_id).get()


def get_black(user_id: int):
    return Blacklist.select().join(User).where(User.vk_id == user_id).get()


def add_to_favorite(
    user_id: int, vk_id: int, first_name: str, last_name: str, city: int, photos: str
):
    fav = Favorite.create(
        user_id=user_id,
        vk_id=vk_id,
        first_name=first_name,
        last_name=last_name,
        city=city,
        photos=photos,
    )
    return fav


def add_to_blacklist(user_id: int, vk_id: int, first_name: str, last_name: str):
    black = Blacklist.create(
        user_id=user_id, vk_id=vk_id, first_name=first_name, last_name=last_name
    )
    return black


def remove_from_fav(user_id: int, vk_id: int):
    return Favorite.delete(vk_id=vk_id).where(User.vk_id == user_id)


def remove_from_black(user_id: int, vk_id: int):
    return Blacklist.delete(vk_id=vk_id).where(User.vk_id == user_id)
