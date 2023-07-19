from config.config import USER_TOKEN
from vkbottle import API
import datetime

api = API(USER_TOKEN)


async def get_photos(user_id):
    try:
        photos = await api.photos.get(
            owner_id=user_id, album_id="profile", count=10, extended=1, photo_sizes=1
        )
        # print(photos.count, photos.items[0].likes)
        # photo_items = photos.items
        photo_items = photos.items

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    user_photos = []
    for photo in photo_items:
        try:
            user_photos.append(
                (
                    photo.likes.count,
                    "photo" + str(photo.owner_id) + "_" + str(photo.id),
                )
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    result = [
        photo
        for photo in user_photos
        if photo[0] not in ["нет фото."] and photo[1] != "нет доступа к фото"
    ]
    photo = sorted(result, reverse=True)
    link_list = [link for _, link in photo]
    return link_list[0:3]


async def search_user(user, offset):
    if user.age is None:
        age_from = 16
        age_to = 100
    else:
        age_from = user.age - 5
        age_to = user.age + 5

    match user.sex:
        case 1:
            sex = 2
        case 2:
            sex = 1
        case _:
            sex = 0

    users = await api.users.search(
        age_from=age_from,
        age_to=age_to,
        sex=sex,
        had_photo=1,
        offset=offset,
        status=1,
    )
    
    return (users.items[0], offset + 1)


async def get_city_id(city_name: str) -> int:
    city = await api.database.get_cities(country_id=1, q=city_name)

    return city.items[0].id if city.items else None


async def get_user_info(user_id):
    fields = ["first_name", "last_name", "id", "sex", "city", "bdate","status"]
    data = await api.users.get(user_id, fields=fields)
    return data[0]


def age_to_int(bdate):
    if bdate == None:
        return None
    today = datetime.date.today()

    born = datetime.datetime.strptime(bdate, "%d.%m.%Y")

    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
