from typing import Union
from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, Message


async def send_forms_answer(bot: Bot,
                            message: Message,
                            data: str,
                            markup: Union[InlineKeyboardMarkup,
                                          ReplyKeyboardMarkup]
                            ) -> None:
    await bot.send_message(
        chat_id=message.chat.id,
        text=data,
        reply_markup=markup
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )

async def edit_callback_message(bot: Bot,
                                callback_query: CallbackQuery,
                                data: str,
                                markup: Union[InlineKeyboardMarkup,
                                              ReplyKeyboardMarkup]
                                ) -> None:
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=data,
                                reply_markup=markup)


async def return_meny_callback(bot: Bot,
                                callback_query: CallbackQuery,
                                markup: Union[InlineKeyboardMarkup,
                                              ReplyKeyboardMarkup]
                                ) -> None:
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=markup)