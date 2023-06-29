from config.config import USER_TOKEN
from vkbottle import API

api = API(USER_TOKEN)


async def get_photos(user_id):
    try:
        photos = await api.photos.get(
            user_id, album_id="profile", count=10, extended=1, photo_sizes=1
        )
        photos = photos.items
    except:
        return None

    user_photos = []
    for i in range(10):
        try:
            user_photos.append(
                photos[i].likes,
                "photo" + str(photos[i].owner_id) + "_" + str(photos[i].id),
            )
        except:
            return None
    result = []
    for photo in user_photos:
        if photo != ["нет фото."] and users_photos != "нет доступа к фото":
            result.append(photo)
    return result



async def search_user(city, offset=0, sex=0, age_from=18, age_to=100):
    users = await api.photos.search(
        city=city, age_from=age_from, age_to=age_to, sex=sex, had_photo=1
    )


async def get_user_info(user_id):
    data = await api.users.get(user_id, fields="first_name,last_name,id,sex,city")
    return data[0]
