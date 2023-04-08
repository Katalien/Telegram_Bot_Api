from aiogram.dispatcher.filters.state import StatesGroup, State
from datetime import datetime

class TaskWithDate(StatesGroup):
    task_text = State()  # Will be represented in storage as 'Form:name'
    date = State()
    repeatable = State()
    period = State()
    notification = State()
    attachments = State()

class TaskEdit(StatesGroup):
    action = State()
    task_id= State()
    period = State()
    task_text = State()
    task_date = State()
    task_notification = State()
    task_done = State()
    task_attachments = State()
    task_return_to_active = State()


class Task(StatesGroup):
    task_text = State()

class TaskDone(StatesGroup):
    task_text = State()

class TaskAddFiles(StatesGroup):
    task_num = State()
    attachments = State()

class TaskReturnToActive(StatesGroup):
    task_text = State()

class TaskAttachment(StatesGroup):
    task_num = State()

class TaskEditText(StatesGroup):
    task_num = State()
    task_text = State()
    period = State()

class TaskEditDate(StatesGroup):
    task_num = State()
    task_date = State()

class TaskEditNotificaion(StatesGroup):
    task_num = State()
    notification = State()


class TaskToDel(StatesGroup):
    task_num = State()
    period = State()