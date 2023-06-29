from vkbottle import Keyboard, KeyboardButtonColor, Text

keyboard = Keyboard(one_time=False)

keyboard.add(Text("Поиск", {"command": "/search"}), color=KeyboardButtonColor.POSITIVE)
keyboard.row()
keyboard.add(
    Text("В избранные", {"command": "/to_fav"}), color=KeyboardButtonColor.POSITIVE
)
keyboard.add(Text("В чс", {"command": "/to_black"}), color=KeyboardButtonColor.POSITIVE)
keyboard.row()
keyboard.add(
    Text("Избранные", {"command": "/show_fav"}), color=KeyboardButtonColor.POSITIVE
)
keyboard.add(
    Text("Blacklist", {"command": "/show_black"}), color=KeyboardButtonColor.POSITIVE
)

keyboard = keyboard.get_json()
