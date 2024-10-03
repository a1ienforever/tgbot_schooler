import re


def get_name(input_str: str):
    pattern = r"Фамилия:\s*(\S+)\nИмя:\s*(\S+)\nОтчество:\s*(\S+)"

    # Поиск данных
    match = re.search(pattern, input_str)

    # Извлечение данных
    if match:
        surname = match.group(1)
        name = match.group(2)
        patronymic = match.group(3)

        # Вывод
        print(f"Фамилия: {surname}\nИмя: {name}\nОтчество: {patronymic}")
        return surname, name, patronymic
    else:
        return 'Данные не найдены', None, None
