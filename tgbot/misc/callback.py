from aiogram.filters.callback_data import CallbackData


class FrameCallback(CallbackData, prefix="frame"):
    type_report: str
    lesson_num: int
    frame: int


class ClassCallback(CallbackData, prefix="class"):
    type_report: str
    lesson_num: int
    class_num: int


class LetterCallback(CallbackData, prefix="letter"):
    type_report: str
    lesson_num: int
    letter: str


class PersonCallback(CallbackData, prefix="person"):
    type_report: str
    person_id: int
