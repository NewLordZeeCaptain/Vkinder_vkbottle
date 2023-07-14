from pprint import pprint
from db.database import *
from keyboard import keyboard
from vkbottle import CtxStorage
from vkbottle.bot import Bot, Message, MessageEvent
from config.config import GROUP_TOKEN, USER_TOKEN

from peewee import IntegrityError
from user_func import *

# GROUP_TOKEN = "vk1.a.7Dxz8HAcsfw8b_qGxDRcEyudtNs9qQp3tYtPxP69Xklhm1vGuVkHk_2ZxARrrNruClP0YFqe41KygfmoTcS-U1fql77I5TIp-cp0Fyuy2Hykf122frZrGEyPv_xocFHubAAPzdxQdgcRpUJpFTqqn21RtqRS_AB52DyZRlOk5HnzL4Fwn3VZJGl5a_i1JA2IjiQu6PhfPmvV7s1l8b5Heg"
# token = SingleTokenGenerator(token=GROUP_TOKEN)


bot = Bot(token=GROUP_TOKEN)
ctx_storage = CtxStorage()




@bot.on.message(text="Начать")
async def begin(message: Message):
    user_info = await get_user_info(message.from_id)

    try:
        status = reg_user(
            vk_id=user_info.id,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            sex=user_info.sex,
            city=user_info.city.id if user_info.city else 1,
            age=age_to_int(user_info.bdate),
        )
        await message.answer(
            f"Добро пожаловать, {user_info.first_name}. Этот бот заменит вам Tinder",
            keyboard=keyboard,
        )
        ctx_storage.set(f"offset_{message.from_id}", 0)
        return True
    except IntegrityError:
        await message.answer(
            f"С возвращением, {user_info.first_name}!", keyboard=keyboard
        )


# @bot.on.message(text="info")
# async def get_info_from_db(message: Message):
#     info = get_user_info_db(message.from_id)
#     await message.answer(
#         f"Info is type of {type(info), info.first_name, info.last_name, info.sex, info.city, info.vk_id}"
#     )

# await message.answer(f"Your info: {info} ")


@bot.on.message(text="Поиск")
async def show_next(message: Message):
    city = get_user_info_db(message.from_id).city
    offset = ctx_storage.get(f"offset_{message.from_id}")
    user = get_user_info_db(message.from_id)
    candidate, offset = await search_user(user=user, offset=offset)

    photos = await get_photos(candidate.id)
    ctx_storage.set(f"offset_{message.from_id}", offset)
    await message.answer(
        f"Here is your candidate: {'https://vk.com/id'+str(candidate.id)}",
        attachment=photos,
        keyboard=keyboard,
    )

    ctx_storage.set(f"candidate_{message.from_id}", candidate)
    ctx_storage.set(f"candidate_photos_{message.from_id}", photos)


@bot.on.message(text="В избранные")
async def add_to_fav(message: Message):
    candidate = ctx_storage.get(f"candidate_{message.from_id}")
    photos = ctx_storage.get(f"candidate_photos_{message.from_id}")
    add_to_favorite(
        user_id=message.from_id,
        vk_id=candidate.id,
        first_name=candidate.first_name,
        last_name=candidate.last_name,
        city=candidate.city,
        photos=candidate.photos,
    )


@bot.on.message(text="В чс")
async def add_to_black(message: Message):
    candidate = ctx_storage.get(f"candidate_{message.from_id}")
    add_to_blacklist(
        user_id=message.from_id,
        vk_id=candidate.id,
        first_name=candidate.first_name,
        last_name=candidate.last_name,
    )


@bot.on.message(text="Избранные")
async def show_fav(message: Message):
    pass


@bot.on.message(text="Blacklist")
async def show_black(message: Message):
    pass


# @bot.on.message(text="photo")
# async def get_photo(message: Message):
#     try:
#         photo = await get_photos(message.from_id)
#         if photo is None:
#             await message.answer("I can't access your photo")
#         else:
#             link_list = [link for _, link in photo]

#             await message.answer(
#                 "Here are some of your photos", keyboard=keyboard, attachment=link_list
#             )
#     except Exception as e:
#         await message.answer(f"An error occurred while fetching photos {e}")
#     # except Exception as e:

#     #     await message.answer("Failed to retrieve photos. Please try again later. With Exception", e)


@bot.on.message()
async def echo_handler(message: Message):
    users_info = await api.users.get(
        message.from_id, fields="first_name,last_name,id,sex"
    )

    await message.answer(
        f"Пользователь {users_info[0].first_name} К сожалению такой команды нет"
    )


bot.run_forever()
