import csv

from tqdm import tqdm

from tgbot.services.db import clear_database_schooler, add_person
from tgbot.utils import split_full_name


async def import_db():
    try:
        clear_database_schooler()
        file_path = input("Путь к файлу: ")
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            total_rows = sum(1 for _ in reader)

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            with tqdm(total=total_rows, desc="Импорт", unit=" записей") as pbar:
                for row in reader:
                    full_name = row[0]
                    class_num = row[1]
                    letter = row[2]
                    building = row[3]

                    last_name, first_name, middle_name = split_full_name(full_name)

                    # Добавляем данные в БД
                    await add_person(
                        first_name=first_name,
                        last_name=last_name,
                        class_num=class_num,
                        letter=letter,
                        building=building,
                        middle_name=middle_name,
                    )

                    pbar.update(1)

            print(f"Импорт завершён. Всего записей: {total_rows}")

    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
