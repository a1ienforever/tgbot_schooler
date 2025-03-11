from icecream import ic

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


async def choose_frame_state(message, text, type_report, lesson_num):
    await message.answer(
        text=text,
        reply_markup=choose_frame_kb(type_report, lesson_num=lesson_num),
    )


async def choose_class_state(type_report, lesson_num, frame, call):
    if frame == 1:
        await call.message.edit_text(
            text="Выберите класс учащихся",
            reply_markup=first_frame_class_kb(type_report, lesson_num),
        )
    if frame == 4:
        await call.message.edit_text(
            text="Выберите класс учащихся",
            reply_markup=second_frame_class_kb(type_report, lesson_num),
        )


async def choose_letter_state(frame, class_num, lesson_num, type_report, call):
    if frame == 1:
        await call.message.edit_text(
            "Выберите букву класса",
            reply_markup=first_frame_letter_kb(
                type_report=type_report, lesson_num=lesson_num
            ),
        )
    elif frame == 4:
        if int(class_num) in [1]:
            await call.message.edit_text(
                "Выберите букву класса",
                reply_markup=generate_eab_kb(
                    type_report=type_report, lesson_num=lesson_num
                ),
            )
        if int(class_num) in [2, 6, 7, 11]:
            await call.message.edit_text(
                "Выберите букву класса",
                reply_markup=generate_a_kb(
                    type_report=type_report, lesson_num=lesson_num
                ),
            )
        if int(class_num) in [3]:
            await call.message.edit_text(
                "Выберите букву класса",
                reply_markup=generate_ea_kb(
                    type_report=type_report, lesson_num=lesson_num
                ),
            )
        if int(class_num) in [4, 5]:
            await call.message.edit_text(
                "Выберите букву класса",
                reply_markup=generate_ab_kb(
                    type_report=type_report, lesson_num=lesson_num
                ),
            )
        if int(class_num) in [8]:
            await call.message.edit_text(
                "Выберите букву класса",
                reply_markup=generate_gnste_kb(
                    type_report=type_report, lesson_num=lesson_num
                ),
            )
        if int(class_num) in [9]:
            await call.message.edit_text(
                "Выберите букву класса",
                reply_markup=generate_gnte_kb(
                    type_report=type_report, lesson_num=lesson_num
                ),
            )
        if int(class_num) in [10]:
            await call.message.edit_text(
                "Выберите букву класса",
                reply_markup=generate_npt_kb(
                    type_report=type_report, lesson_num=lesson_num
                ),
            )
