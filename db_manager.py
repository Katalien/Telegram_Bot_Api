import datetime
from models import *
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

with db:
    db.create_tables([Task])
    # hw = Task(user_id=1, task_text="do nomework").save()
    # hw = Task( task_text="do nomework").save()
    # dance = Task.create(task_text='dance today')
    # bot = Task.insert(task_text='complete bot').execute()
print('Done')

# def insert(user_id: int, new_task_name: str, new_task_date: datetime, notification: datetime, ) -> object:
#     new_task = Task(task_text=new_task_name).save()
#     print("You saved task")
#     return new_task

def insert(new_item: Dict) -> object:
    task = Task(user_id = new_item['user_id'],
                task_text = new_item['task_text'],
                task_date = new_item['date'],
                notification_time = new_item['notification'],
                repeat_min = new_item["repeat"],
                attachments = new_item["attachments"]
               )
    print(new_item['notification'])
    task.save()
    return task

def saveTask(task):
    task.save()
    return task

def fetchAll(user_id: int):
    tasks_sql = Task.select().where(Task.user_id == user_id)
    return list(tasks_sql)

def fetchActiveTasks(user_id: int):
    tasks = Task.select().where(Task.completed == False, Task.user_id == user_id)
    return list(tasks)

def fetchCompletedTasks(user_id: int):
    tasks = Task.select().where(Task.completed == True, Task.user_id == user_id)
    return list(tasks)

def fetchPeriodicalTasks(user_id: int):
    tasks = Task.select().where(Task.repeat_min != None, Task.user_id == user_id)
    return list(tasks)

def fetchAttachmentsTasks(task_id: int, user_id: int):
    tasks = Task.select().where(Task.attachments == True, Task.user_id == user_id, Task.id == task_id)
    return list(tasks)

def make_completed(id: int, date: datetime, user_id: int):
    task = Task.update(completed = True, date_completed = date).where(Task.id == id, Task.user_id == user_id)
    task.execute()

def edit_text(id: int, new_text: str, user_id: int):
    task = Task.update(task_text = new_text).where(Task.id == id, Task.user_id == user_id)
    task.execute()

def edit_date(id: int, new_date, user_id: int):
    task = Task.update(task_date = new_date).where(Task.id == id, Task.user_id == user_id)
    task.execute()

def delete_by_id(id: int, user_id: int):
    task_to_del = Task.get(Task.id == id, Task.user_id == user_id)
    task_text = task_to_del.task_text
    date = task_to_del.task_date
    notification = task_to_del.notification_time
    completed = task_to_del.completed
    task_to_del.delete_instance()
    return task_text, date, notification, completed

def find_by_date(date: str, user_id: int) -> List:
    tasks = Task.select().where(Task.task_date == date, Task.user_id == user_id)
    return list(tasks)

def find_by_notification(date: str) -> List:
    tasks = Task.select().where(Task.notification_time == date)
    return list(tasks)

def find_by_id(id: int, user_id: int) -> object:
    task = Task.get(Task.id == id, Task.user_id == user_id)
    return task

def edit_task_notification(id, new_notification):
    print(new_notification)
    tasks = Task.select().where(Task.id == id)
    for task in tasks:
        task.notification_time = new_notification
        task.save()

def null_notification(id):
    task = Task(notification_time=None)
    task.id = id
    task.save()

def edit_task_notification_by_id(id, new_notification):
    task = Task(notification_time = new_notification)
    task.id = id
    task.save()

def edit_task_date_by_id(id, new_date):
    task = Task(task_date = new_date)
    task.id = id
    task.save()

def update_date(id: int, user_id: int):
    task = find_by_id(id, user_id)
    old_date = task.task_date
    new_date = old_date + timedelta(minutes=task.repeat_min)
    task = Task.update(task_date=new_date).where(Task.id == id, Task.user_id == user_id)
    task.execute()

def make_task_active(id:int, user_id: int):
    task = Task.update(completed = False, date_completed = None).where(Task.id == id, Task.user_id == user_id)
    task.execute()

def change_attachments(task_id, user_id):
    task = Task(attachments=True)
    task.id = task_id
    task.save()