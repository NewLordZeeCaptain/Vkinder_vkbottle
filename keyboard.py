from vkbottle import Keyboard, KeyboardButtonColor, Text

keyboard = Keyboard(one_time=False)

keyboard.add(Text("Поиск", {"command": "/search"}), color=KeyboardButtonColor.PRIMARY)

keyboard = keyboard.get_json()
