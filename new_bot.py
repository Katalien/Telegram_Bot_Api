import asyncio
import os
import time
import aioschedule
import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as md
from aiogram.types import update, ContentTypes
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import db_manager
import keyboard as kb
import message_manager
import server
import re
from TasksTypes import *
from datetime import datetime, timedelta
import bot_answers
from server import *


# parse date in fedruary
# edit date but do no edit notification date/ No error but it is missing ib a list of all tasks
#

TOKEN = "5870625403:AAHbyqr1XSX3P9U9W8-etfwvp-xKSU7loZk"
MSG = "Hi there! I will help you remember everything you want"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message_handler(lambda message: message.text == "Add new task")
async def add_new_task(message: types.Message):
    await message.answer("Type your task\n\nIf you have changed your mind about creating a task, type -")
    await TaskWithDate.task_text.set()

@dp.message_handler(state=TaskWithDate.task_text)
async def fill_new_task_text(message: types.Message, state: FSMContext):
    text = message.text.rstrip()
    if text == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_start)
        await state.finish()
        return
    async with state.proxy() as data:
        data["task_text"] = text
    await message.answer("Type date in one of the formats below\n\n" + message_manager.emoji_date + "dd/mm/yy\n" + message_manager.emoji_date + "dd/mm/yy mm:hh\n\nIf task has no date type -")
    await TaskWithDate.next()

@dp.message_handler(state=TaskWithDate.date)
async def fill_new_task_date(message: types.Message, state: FSMContext):
    date = message.text
    async with state.proxy() as data:
        if date == '-':
            data['date'] = None
        else:
            datetime_object = server.check_date(date)
            if isinstance(datetime_object, str):
                await bot.send_message(message.from_user.id, datetime_object)
            else:
                data["date"] = datetime_object
    if data["date"] != None:
        await message.answer("Repeat this task?", reply_markup=kb.repeat_kb)
        await TaskWithDate.next()
    else:
        async with state.proxy() as data:
            data["repeatable"] = "no_repeat"
        await TaskWithDate.next()
        async with state.proxy() as data:
            data["period"] = None
        await TaskWithDate.next()
        async with state.proxy() as data:
            data["notification"] = "no notify"
        await bot.send_message(chat_id=message.from_user.id, text="Attach files", reply_markup=kb.kb_no_attach)
        await TaskWithDate.attachments.set()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "hour"
                             or callback_query.data == "day"
                            or callback_query.data == "week"
                            or callback_query.data == "month",
                           state=TaskWithDate.repeatable)
async def fill_new_task_repetition(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
            data["repeatable"] = callback.data
    await bot.send_message(chat_id=callback.from_user.id, text="Type the period of repetition\n\ne.x. type '2' if you want to repeat it every 2 (hours/days/...) ")
    await TaskWithDate.next()

@dp.message_handler(state=TaskWithDate.period)
async def fill_new_task_frequency_of_repetition(message: types.Message, state: FSMContext):
    period = message.text
    async with state.proxy() as data:
            data["period"] = period
    await message.answer("Notification?", reply_markup=kb.notification_kb)
    await TaskWithDate.next()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "no_repeat", state=TaskWithDate.repeatable)
async def process_new_task_repetition(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
            data["repeatable"] = "no_repeat"
    await TaskWithDate.next()
    async with state.proxy() as data:
            data["period"] = None
    await bot.send_message(chat_id=callback.from_user.id, text="Remind you about it?", reply_markup=kb.notification_kb)
    await TaskWithDate.next()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "10 minutes"
                             or callback_query.data == "30 minutes"
                            or callback_query.data == "1 hour"
                            or callback_query.data == "1 day"
                            or callback_query.data == "no notify",
                           state=TaskWithDate.notification)
async def fill_new_task_notification(callback: types.CallbackQuery, state: FSMContext):
    notification = callback.data
    async with state.proxy() as data:
            data["notification"] = notification
    await bot.send_message(chat_id=callback.from_user.id, text="Attach files", reply_markup=kb.kb_no_attach)
    await TaskWithDate.next()

@dp.message_handler(state=TaskWithDate.attachments, content_types=types.ContentType.DOCUMENT)
async def fill_new_task_attachments(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        file_dir = data['task_text']
    if len(file_dir) > 20:
        file_dir = file_dir[0:20]
    file_id = message.document.file_id
    print(file_id)
    file = await bot.get_file(file_id)
    filename = message.document.file_name
    if not os.path.isdir(f"attachments/" + str(message.from_user.id)):
        os.makedirs(f"attachments/" + str(message.from_user.id) + "/" + file_dir +"/" )
    # await file.download(destination=f"attachments/{filename}")
    await file.download(destination=f"attachments/" + str(message.from_user.id) + "/" + file_dir +"/" + f"{filename}")
    async with state.proxy() as data:
        data["attachments"] = str(message.from_user.id) + "/" + file_dir
    await bot.send_message(chat_id=message.from_user.id, text="File was added. Add one more or click done.", reply_markup=kb.kb_done)

@dp.message_handler(lambda message: message.text == "No attach", state=TaskWithDate.attachments)
async def add_task_with_no_files(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["attachments"] = None
    server.add_task_to_db(callback.from_user.id, data)
    await state.finish()
    await bot.send_message(chat_id=callback.from_user.id, text="Task was added", reply_markup=kb.kb_start)

@dp.message_handler(lambda message: message.text == "That's all", state=TaskWithDate.attachments)
async def process_addig_attachments(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        print(data)
    id = server.add_task_to_db(callback.from_user.id, data)
    old_file_dir = f"attachments/" + str(callback.from_user.id) + "/" + str(data['task_text'][0:20])
    new_file_dir = "attachments/" + str(callback.from_user.id) + "/" + str(id)
    os.rename(old_file_dir, new_file_dir)
    await state.finish()
    await bot.send_message(chat_id=callback.from_user.id, text="Task was added", reply_markup=kb.kb_start)

##########

@dp.message_handler(lambda message: message.text == "Back to menu")
async def back_to_menu(message: types.Message):
    await message.reply("Menu", reply_markup=kb.kb_start)

# SHOW TASKS
@dp.message_handler(lambda message: message.text == "Show tasks")
async def show_tasks_menu(message: types.Message):
    await bot.send_message(message.from_user.id, "Choose tasks to show", reply_markup=kb.kb_show)


@dp.message_handler(lambda message: message.text == "Show all tasks")
async def show_all_tasks(message: types.Message):
    tasks = server.find_active_tasks(message.from_user.id)
    mes_with_tasks = message_manager.all_tasks_message(tasks)
    print(mes_with_tasks)
    await message.reply(f"Tasks: {mes_with_tasks}", reply_markup=kb.kb_show)

@dp.message_handler(lambda message: message.text == "Show completed tasks")
async def show_completed_tasks(message: types.Message):
    tasks = server.find_completed_tasks(message.from_user.id)
    mes_with_tasks = message_manager.all_tasks_message(tasks)
    print(mes_with_tasks)
    await message.reply(f"Tasks: {mes_with_tasks}", reply_markup=kb.inline_kb_return)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "return_to_active")
async def return_task_to_active(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Type the number of the task.\n\nIf you've changed your mind about returning task to active type -")
    await TaskReturnToActive.task_text.set()

@dp.message_handler(state=TaskReturnToActive.task_text)
async def fill_return_to_active_task_id(message: types.Message, state: FSMContext):
    num = message.text
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_show)
        await state.finish()
        return
    async with state.proxy() as data:
        data["task_text"] = num
    db_manager.make_task_active(num, message.from_user.id)
    await state.finish()
    await message.reply("Task is active again", reply_markup=kb.kb_show)

@dp.message_handler(lambda message: message.text == "Show periodical tasks")
async def show_periodical_tasks(message: types.Message):
    tasks = server.find_periodical_tasks(message.from_user.id)
    mes_with_tasks = message_manager.all_tasks_message(tasks)
    await message.reply(f"Tasks: {mes_with_tasks}", reply_markup=kb.kb_show)

@dp.message_handler(lambda message: message.text == "Show attachments")
async def show_attachments_btn(message: types.Message):
    mes = message_manager.all_tasks_message(db_manager.fetchAll(message.from_user.id))
    await bot.send_message(message.from_user.id, mes + "\n\nChose task to show attachments.\n\nIf you don't want to see files type -")
    await TaskAttachment.task_num.set()

@dp.message_handler(state=TaskAttachment.task_num)
async def choose_task_to_show_attachments(message: types.Message, state: FSMContext):
    num = message.text
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_show)
        await state.finish()
        return
    async with state.proxy() as data:
        data["task_num"] = num
    cur_task = db_manager.find_by_id(num, message.from_user.id)
    if cur_task == None:
        await bot.send_message(chat_id=message.from_user.id, text="No such task. Try again ot type - to cancel")
    else:
        task = server.find_task_with_attachments(num, message.from_user.id)
        if task == None:
            await bot.send_message(message.from_user.id, "No files", reply_markup=kb.kb_show)
            await state.finish()
            return
        files_dir = server.get_file_dir(num, message.from_user.id)
        await bot.send_message(message.from_user.id, message_manager.all_tasks_message(task))
        if files_dir == None:
            await bot.send_message(message.from_user.id, "No files")
            await state.finish()
            return
        else:
            for file_name in os.listdir(files_dir):
                file_path = os.path.join(files_dir, file_name)
                with open(file_path, "rb") as file:
                    await bot.send_document(message.chat.id, file)
        await state.finish()
        await bot.send_message(message.from_user.id, "Here you are", reply_markup=kb.kb_show)

# Delete task function
@dp.message_handler(lambda message: message.text == "Delete task")
async def choose_task_to_delete(message: types.Message):
    mes = message_manager.all_tasks_message(db_manager.fetchAll(message.from_user.id))
    await bot.send_message(message.from_user.id, mes + "\n\nChose task to delete\n\nIf you don't want to delete anything type -")
    await TaskToDel.task_num.set()

@dp.message_handler(state=TaskToDel.task_num)
async def delete_task(message: types.Message, state: FSMContext):
    num = message.text
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_edit)
        await state.finish()
        return
    async with state.proxy() as data:
        data["task_num"] = num
    task = db_manager.find_by_id(num, message.from_user.id)
    if task == None:
        await bot.send_message(message.from_user.id, "No such task. Try again or type - to cancel")
        return
    if task.repeat_min != None:
        await message.reply( text="Task is periodical. Do you want to delete it once?", reply_markup=kb.inline_kb_yes_no)
        await TaskToDel.period.set()
    else:
        server.delete_task_files(num, message.from_user.id)
        db_manager.delete_by_id(num, message.from_user.id)
        await state.finish()
        await message.reply( text="Task was deleted", reply_markup=kb.kb_start)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "yes_once"
                                                  or callback_query.data == "no_periodicaly",
                                                  state=TaskToDel.period)
async def delete_periodical_task(callback: types.CallbackQuery, state: FSMContext):
    period = callback.data
    async with state.proxy() as data:
        data["period"] = period
        task_id = data["task_num"]
    server.delete_task_files(task_id, callback.from_user.id)
    server.delete_periodical_task(data, callback.from_user.id)
    await state.finish()
    await bot.send_message(callback.from_user.id, "deleted", reply_markup=kb.kb_edit)


# Edit task functions
@dp.message_handler(lambda message: message.text == "Edit task")
async def edit_task_menu(message: types.Message):
    mes = message_manager.all_tasks_message(server.find_active_tasks(message.from_user.id))
    await bot.send_message(message.from_user.id, mes + "\n\nChoose action to do", reply_markup=kb.kb_edit)

@dp.message_handler(lambda message: message.text == "Make Done")
async def choose_task_to_make_done(message: types.Message):
    await bot.send_message(message.from_user.id, "What task is completed?\nIf you don't want to make any task completed type -")
    await TaskDone.task_text.set()

@dp.message_handler(state=TaskDone.task_text)
async def make_task_done(message: types.Message, state: FSMContext):
    num = message.text
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_edit)
        await state.finish()
        return
    async with state.proxy() as data:
        data["task_text"] = num
    task = db_manager.find_by_id(num, message.from_user.id)
    if task == None:
        await bot.send_message(message.from_user.id, "No such task. Try again\n\nType - to cancel editing")
        return
    local_time = str(datetime.now())[:-9] + "00"
    task = db_manager.make_completed( data["task_text"], local_time, message.from_user.id)
    await state.finish()
    await message.reply("Completed", reply_markup=kb.kb_edit)

@dp.message_handler(lambda message: message.text == "Edit description")
async def edit_decription_btn(message: types.Message):
    await bot.send_message(message.from_user.id, "What is the task to edit?\n\nType - to cancel editing")
    await TaskEditText.task_num.set()

#  edit task text
@dp.message_handler(state=TaskEditText.task_num)
async def choose_task_to_edit_description(message: types.Message, state: FSMContext):
    num = message.text
    async with state.proxy() as data:
        data["task_num"] = num
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_edit)
        await state.finish()
        return
    task = db_manager.find_by_id(num, message.from_user.id)
    if task == None:
        await bot.send_message(message.from_user.id, "No such task. Try again or type - to cancel")
        return
    mes = str(task.task_text) + "\n\n What is a new task text?"
    await message.answer(mes)
    await TaskEditText.next()


@dp.message_handler(state=TaskEditText.task_text)
async def edit_description(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data["task_text"] = text
    task = db_manager.find_by_id(data['task_num'], message.from_user.id)
    if task.repeat_min != None:
        await message.answer("Only once?", reply_markup=kb.inline_kb_yes_no)
        await TaskEditText.next()
    else:
        await TaskEditText.next()
        async with state.proxy() as data:
            data["period"] = None
        task = db_manager.edit_text(data["task_num"], data['task_text'], message.from_user.id)
        await state.finish()
        await bot.send_message(message.from_user.id, "Done", reply_markup=kb.kb_edit)



@dp.callback_query_handler(lambda callback_query: callback_query.data == "yes_once"
                            or callback_query.data == "no_periodicaly",
                            state=TaskEditText.period)
async def periodical_task_edit_description(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["period"] = callback.data
    if callback.data == "yes_once":
        task = server.edit_task_text_once(data['task_num'], data['task_text'], callback.from_user.id)

    elif callback.data == "no_periodicaly":
        task = server.edit_task_text_always(data['task_num'], data['task_text'], callback.from_user.id)
    await state.finish()
    await bot.send_message(callback.from_user.id, "Done", reply_markup=kb.kb_edit)

#  Edit files
@dp.message_handler(lambda message: message.text == "Add files")
async def add_files_btn(message: types.Message):
    await bot.send_message(message.from_user.id, "Choose task to add files. \n Type - to cancel")
    await TaskAddFiles.task_num.set()

@dp.message_handler(state=TaskAddFiles.task_num)
async def choose_task_to_add_files(message: types.Message, state: FSMContext):
    num = message.text
    async with state.proxy() as data:
        data["task_num"] = num
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_edit)
        await state.finish()
        return
    task = db_manager.find_by_id(num, message.from_user.id)
    if task == None:
        await bot.send_message(message.from_user.id, "No such task. Try again\n\nType - to cancel editing")
        return
    await bot.send_message(message.from_user.id, "Attach files or click done", reply_markup=kb.kb_done)
    await TaskAddFiles.next()

@dp.message_handler(state=TaskAddFiles.attachments, content_types=types.ContentType.DOCUMENT)
async def add_files_process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        task_id = data['task_num']
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    filename = message.document.file_name
    if not os.path.isdir(f"attachments/" + str(message.from_user.id)):
        os.makedirs(f"attachments/" + str(message.from_user.id) + "/" + str(task_id) +"/" )
    # await file.download(destination=f"attachments/{filename}")
    await file.download(destination=f"attachments/" + str(message.from_user.id) + "/" + str(task_id) +"/" + f"{filename}")
    async with state.proxy() as data:
        data["attachments"] = str(message.from_user.id) + "/" + str(task_id)
    # await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text="File was added. Add one more or click done.", reply_markup=kb.kb_done)

@dp.message_handler(lambda message: message.text == "That's all", state=TaskAddFiles.attachments)
async def done_adding(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        print(data)
    task_id = data["task_num"]
    await state.finish()
    task = db_manager.find_by_id(task_id, callback.from_user.id)
    if task.attachments == False:
        server.change_attachments_status(task_id, callback.from_user.id)
    await bot.send_message(chat_id=callback.from_user.id, text="Done", reply_markup=kb.kb_start)

#  Edit date
@dp.message_handler(lambda message: message.text == "Edit date")
async def edit_date_btn(message: types.Message):
    await bot.send_message(message.from_user.id, "What is the task to edit?\nType - to cancel editing")
    await TaskEditDate.task_num.set()

@dp.message_handler(state=TaskEditDate.task_num)
async def choose_task_to_edit_date(message: types.Message, state: FSMContext):
    num = message.text
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_edit)
        await state.finish()
        return
    async with state.proxy() as data:
        data["task_num"] = num
    task = db_manager.find_by_id(num, message.from_user.id)
    if task == None:
        await bot.send_message(message.from_user.id, "No such task. Try again or type - to cancel editing")
        return
    task = db_manager.find_by_id(num, message.from_user.id)
    mes = str(task.task_date) + "\n\nWhat is a new date?\n" + message_manager.emoji_date + "dd/mm/yy\n" + message_manager.emoji_date + "dd/mm/yy hh:mm\n\nIf task has no date type -"
    await message.answer(mes)
    await TaskEditDate.next()

@dp.message_handler(state=TaskEditDate.task_date)
async def process_new_date(message: types.Message, state: FSMContext):
    date = message.text
    async with state.proxy() as data:
        if date == '-':
            data['date'] = None
        else:
            datetime_object = server.check_date(date)
            if isinstance(datetime_object, str):
                await bot.send_message(message.from_user.id, datetime_object)
                return
            else:
                data["date"] = datetime_object
    server.edit_date(data["task_num"],  data["date"], message.from_user.id)
    # task = db_manager.edit_task_date_by_id(data["task_num"],  data["date"])
    await state.finish()
    await message.reply("Done", reply_markup=kb.kb_edit)


# Edit notification
@dp.message_handler(lambda message: message.text == "Edit notification")
async def edit_notification(message: types.Message):
    await bot.send_message(message.from_user.id, "What is the task to edit?\nType - to cancel")
    await TaskEditNotificaion.task_num.set()

@dp.message_handler(state=TaskEditNotificaion.task_num)
async def choose_task_to_edit_notification(message: types.Message, state: FSMContext):
    num = message.text
    if num == "-":
        await bot.send_message(chat_id=message.from_user.id, text="Cancel", reply_markup=kb.kb_edit)
        await state.finish()
        return
    async with state.proxy() as data:
        data["task_num"] = num
    task = db_manager.find_by_id(num, message.from_user.id)
    if task == None:
        await bot.send_message(chat_id=message.from_user.id, text="No such task. Try again",
                               reply_markup=kb.kb_edit)
        return
    if task.task_date == None:
        await bot.send_message(chat_id=message.from_user.id, text="Task has no date. You can't add notification", reply_markup=kb.kb_edit)
        await state.finish()
        return
    elif task.notification_time == None:
        mes = "Task date: " + str(task.task_date) + "\n"
        mes += "No notification"
    else:
        mes = str(task.task_date) + "\n"
        mes += message_manager.make_mes_notification_from_task(task)
    mes += "\n\n What is a new notification?"
    await message.answer(mes, reply_markup=kb.notification_kb)
    await TaskEditNotificaion.next()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "10 minutes"
                             or callback_query.data == "30 minutes"
                            or callback_query.data == "1 hour"
                            or callback_query.data == "1 day"
                            or callback_query.data == "no notify",
                           state=TaskEditNotificaion.notification)
async def process_notification(callback: types.CallbackQuery, state: FSMContext):
    notification = callback.data
    async with state.proxy() as data:
            data["notification"] = notification
    server.edit_task_notification(data['task_num'], notification, callback.from_user.id)
    await state.finish()
    await bot.send_message(chat_id=callback.from_user.id, text="Notification was changed", reply_markup=kb.kb_start)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    meet_message = "Hi there! I am RomKa and I will help you to remember everything. Have fun:)"
    await message.reply(meet_message + "\n\nMenu", reply_markup=kb.kb_start)

async def notify():
    local_time = str(datetime.now())[:-9] + "00"
    all_tasks = db_manager.find_by_notification(local_time)
    i = 1
    if len(all_tasks) != 0:
        for task in all_tasks:
            print(i)
            i+=1
            message = message_manager.mes_from_task(task)
            await bot.send_message(chat_id=task.user_id, text=message)
            if task.repeat_min is not None:
                new_notification = datetime.now() + timedelta(minutes=task.repeat_min)
                new_notification = str(new_notification)[:-9] + "00"
                datetime_object = datetime.strptime(new_notification, '%Y-%m-%d %H:%M:%S')
                db_manager.edit_task_notification_by_id(task.id, datetime_object)
                new_date = task.task_date + timedelta(minutes=task.repeat_min)
                db_manager.edit_task_date_by_id(task.id, new_date)

async def send_tasks():
    aioschedule.every(58).seconds.do(notify)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(send_tasks())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)