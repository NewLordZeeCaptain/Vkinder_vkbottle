from pprint import pprint
from db.database import *
from keyboard import keyboard
from vkbottle import CtxStorage
from vkbottle.bot import Bot, Message, MessageEvent
from config.config import GROUP_TOKEN, USER_TOKEN

from peewee import IntegrityError
from user_func import *


bot = Bot(token=GROUP_TOKEN)
ctx_storage = CtxStorage()


@bot.on.message(text="Начать")
async def begin(message: Message):
    user_info = await get_user_info(message.from_id)

    try:
        status = reg_user(
            user_id=user_info.id,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            sex=user_info.sex,
            city=user_info.city.id if user_info.city else 1,
            age=age_to_int(user_info.bdate),
            status=user_info.status if user_info.status else 1,
        )
        ctx_storage.set(f"offset_{message.from_id}", 0)
        await message.answer(
            f"Добро пожаловать, {user_info.first_name}. Этот бот заменит вам Tinder",
            keyboard=keyboard,
        )

        if not user_info.city:
            await message.answer(questions["city"]["question"])
            ctx_storage.set(f"awaiting_{message.from_id}", "city")
        elif not user_info.status:
            await message.answer(questions["status"]["question"])
            ctx_storage.set(f"awaiting_{message.from_id}", "status")
        elif not user_info.bdate:
            await message.answer(questions["bdate"]["question"])
            ctx_storage.set(f"awaiting_{message.from_id}", "bdate")

    except IntegrityError:
        await message.answer(
            f"С возвращением, {user_info.first_name}!", keyboard=keyboard
        )


@bot.on.message(
    func=lambda message: ctx_storage.get(f"awaiting_bdate_{message.from_id}")
)
async def handle_bdate(message: Message):
    bdate = message.text
    user_id = message.from_id
    age = age_to_int(bdate)
    update_age(user_id, age)
    await message.answer(f"Age is set to {age}", keyboard=keyboard)



@bot.on.message(
    func=lambda message: ctx_storage.get(f"awaiting_status_{message.from_id}")
)
async def handle_status(message: Message):
    status = message.text
    user_id = message.from_id
    try:
        status = int(status)
    except:
        await message.answer("Это должно быть число")
        return
    if 0 > status > 7:
        await message.answer(f"Такого статуса нет")
        return
    update_status(user_id, status)
    await message.answer(f"Status is set to {status}", keyboard=keyboard)



@bot.on.message(
    func=lambda message: ctx_storage.get(f"awaiting_city_{message.from_id}")
)
async def handle_city(message: Message):
    city = message.text
    user_id = message.from_id
    city_id = await get_city_id(city)

    if city_id == None:
        await message.answer(f"Такого города нет")
        return
    update_city(user_id, city_id)
    await message.answer(f"City is set to {city}", keyboard=keyboard)



questions = {
    "city": {
        "question": "Enter your city:",
        "handler": handle_city,
        "next": "status",
    },
    "status": {
        "question": "Enter your status (1 - Single, 2 - Dating, 3 - помолвлен(а), 4 - женат\замужем, 5 - всё сложно, 6 - Active Search, 7 - In Love, 8 - Гражданский брак):",
        "handler": handle_status,
        "next": "bdate",
    },
    "bdate": {
        "question": "Enter your birthdate: dd.mm.yyyy format",
        "handler": handle_bdate,
        "next": None,
    },
}


@bot.on.message(text="Поиск")
async def show_next(message: Message):
    user = get_user_info_db(message.from_id)
    offset = ctx_storage.get(f"offset_{message.from_id}")
    candidate = None
    while candidate is None or candidate.is_closed:
        candidate, offset = await search_user(user=user, offset=offset)
    photos = await get_photos(candidate.id)
    ctx_storage.set(f"offset_{message.from_id}", offset)
    await message.answer(
        f"Here is your candidate: Firstname: {candidate.first_name} Lustname: {candidate.last_name} URL: {'https://vk.com/id'+str(candidate.id)}",
        attachment=photos,
        keyboard=keyboard,
    )


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

@bot.on.message()
async def handle_question(message: Message):
    user_id = message.from_id
    question_key = ctx_storage.get(f"awaiting_{user_id}")
    if question_key is None:
        return
    question = questions[question_key]
    await question["handler"](message)
    next_question_key = question["next"]
    if next_question_key is not None:
        next_question = questions[next_question_key]
        await message.answer(next_question["question"])
        ctx_storage.set(f"awaiting_{user_id}", next_question_key)
    else:
        ctx_storage.delete(f"awaiting_{user_id}")
        
@bot.on.message()
async def echo_handler(message: Message):
    users_info = await api.users.get(
        message.from_id, fields="first_name,last_name,id,sex"
    )

    await message.answer(
        f"Пользователь {users_info[0].first_name} К сожалению такой команды нет"
    )


bot.run_forever()
