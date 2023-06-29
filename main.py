from pprint import pprint
from db.database import *
from keyboard import keyboard
from vkbottle.bot import Bot, Message
from config.config import GROUP_TOKEN, USER_TOKEN
from peewee import IntegrityError
from user_func import *

# GROUP_TOKEN = "vk1.a.7Dxz8HAcsfw8b_qGxDRcEyudtNs9qQp3tYtPxP69Xklhm1vGuVkHk_2ZxARrrNruClP0YFqe41KygfmoTcS-U1fql77I5TIp-cp0Fyuy2Hykf122frZrGEyPv_xocFHubAAPzdxQdgcRpUJpFTqqn21RtqRS_AB52DyZRlOk5HnzL4Fwn3VZJGl5a_i1JA2IjiQu6PhfPmvV7s1l8b5Heg"
# token = SingleTokenGenerator(token=GROUP_TOKEN)


bot = Bot(token=GROUP_TOKEN)


@bot.on.message(payload="/search")
@bot.on.message(text="Начать")
async def begin(message: Message):
    user_info = await get_user_info(message.from_id)

    try:
        status = reg_user(
            vk_id=user_info.id,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            sex=user_info.sex,
        )
        await message.answer(
            f"Добро пожаловать, {user_info.first_name}. Этот бот заменит вам Tinder",
            keyboard=keyboard,
        )
    except IntegrityError:
        await message.answer(
            f"С возвращением, {user_info.first_name}!", keyboard=keyboard
        )


@bot.on.message(text="info")
async def get_info_from_db(message: Message):
    info = get_user_info_db(message.from_id)
    await message.answer(
        f"Info is type of {type(info), info.first_name, info.last_name}"
    )

    # await message.answer(f"Your info: {info} ")


@bot.on.message(text="Поиск")
async def show_next(message: Message):
    pass


@bot.on.message(text="В избранные")
async def add_to_fav(message: Message):
    pass


@bot.on.message(text="В чс")
async def add_to_black(message: Message):
    pass


@bot.on.message(text="Избранные")
async def show_fav(message: Message):
    pass


@bot.on.message(text="Blacklist")
async def show_black(message: Message):
    pass


@bot.on.message(text="photo")
async def get_photo(message: Message):
    # try:
    photo = await get_photos(message.from_id)
    await message.answer(
        "Here is some of your photos", keyboard=keyboard, attachment=photo
    )
    # except Exception as e:

    #     await message.answer("Failed to retrieve photos. Please try again later. With Exception", e)


@bot.on.message()
async def echo_handler(message: Message):
    users_info = await api.users.get(
        message.from_id, fields="first_name,last_name,id,sex"
    )

    await message.answer(
        f"Пользователь {users_info[0].first_name} К сожалению такой команды нет"
    )


bot.run_forever()
