from vkbottle import Keyboard, KeyboardButtonColor, Text

keyboard = Keyboard(one_time=False)

keyboard.add(Text("Поиск", {"command": "/search"}), color=KeyboardButtonColor.PRIMARY)
# keyboard.row()
# keyboard.add(
#     Text("В избранные", {"command": "/to_fav"}), color=KeyboardButtonColor.SECONDARY
# )
# keyboard.add(
#     Text("В чс", {"command": "/to_black"}), color=KeyboardButtonColor.SECONDARY
# )
# keyboard.row()
# keyboard.add(
#     Text("Избранные", {"command": "/show_fav"}), color=KeyboardButtonColor.NEGATIVE
# )
# keyboard.add(
#     Text("Blacklist", {"command": "/show_black"}), color=KeyboardButtonColor.NEGATIVE
# )
# keyboard.row()
# keyboard.add(
#     Text("Настройки", {"command": "/config"}), color=KeyboardButtonColor.POSITIVE
# )
keyboard = keyboard.get_json()
