from tgbot.keyboards.inline import (
    first_frame_class_kb,
    second_frame_class_kb,
    first_frame_letter_kb,
    generate_eab_kb,
    generate_a_kb,
    generate_ea_kb,
    generate_ab_kb,
    generate_gnste_kb,
    generate_gnte_kb,
    generate_npt_kb,
    choose_frame_kb,
)
from tgbot.misc.states import IncidentForm


async def choose_frame_state(message, lesson_num):
    await message.answer(
        "Пожалуйста выберите корпус учащихся",
        reply_markup=choose_frame_kb(lesson_num=lesson_num),
    )


async def choose_class_state(frame: str, call):
    if frame == "1":
        await call.message.edit_text(
            "Выберите класс учащихся", reply_markup=first_frame_class_kb()
        )
    if frame == "4":
        await call.message.edit_text(
            "Выберите класс учащихся", reply_markup=second_frame_class_kb()
        )


async def choose_letter_state(frame, class_num, call):

    if frame == "1":
        await call.message.edit_text(
            "Выберите букву класса", reply_markup=first_frame_letter_kb()
        )
    elif frame == "4":
        if int(class_num) in [1]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_eab_kb()
            )
        if int(class_num) in [2, 6, 7, 11]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_a_kb()
            )
        if int(class_num) in [3]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_ea_kb()
            )
        if int(class_num) in [4, 5]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_ab_kb()
            )
        if int(class_num) in [8]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_gnste_kb()
            )
        if int(class_num) in [9]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_gnte_kb()
            )
        if int(class_num) in [10]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_npt_kb()
            )


async def choose_back(frame, call):

    if frame == "4":
        await call.message.edit_text(
            "Выберите класс учащихся", reply_markup=second_frame_class_kb()
        )
    if frame == "1":
        await call.message.edit_text(
            "Выберите класс учащихся", reply_markup=first_frame_class_kb()
        )
    return
