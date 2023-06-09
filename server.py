import shutil
import db_manager
import message_manager
from datetime import datetime, timedelta
import re

def procces_repeat_period(data):
    if data["repeatable"] == "no_repeat":
        return None
    period = 0
    if data["repeatable"] == "hour":
       period = int(data["period"]) * 60
    if data["repeatable"] == "day":
       period = int(data["period"]) * 24 * 60
    if data["repeatable"] == "week":
       period = int(data["period"]) * 7 * 24 * 60
    if data["repeatable"] == "month":
       period = int(data["period"]) * 31 * 24 * 60
    return period

def get_notification_date(data):
    if data["date"] == None:
        return None
    if data["notification"] == "no notify":
        return None
    # period = procces_repeat_period(data)
    if data["notification"] == "10 minutes":
        return data["date"] - timedelta(minutes=10)
    if data["notification"] == "30 minutes":
        return data["date"] - timedelta(minutes=30)
    if data["notification"] == "1 hour":
        return data["date"] - timedelta(hours=1)
    if data["notification"] == "1 day":
        return data["date"] - timedelta(days=1)
    if data["notification"] == "no notify":
        return None

def add_task_to_db(user_id, data):
    task_text = data['task_text']
    if 'date' in data:
        date = data['date']
    else:
        date = None
    if 'notification' in data:
        notification = get_notification_date(data)
    else:
        notification = None
    if data['attachments'] != None:
        attachments = True
    else:
        attachments = False
    print(notification)
    item = {"user_id": user_id, "task_text": task_text, "date": date, "notification": notification,
            "repeat": procces_repeat_period(data), "attachments": attachments }
    return db_manager.insert(item)

def find_periodical_tasks(user_id: int):
    return db_manager.fetchPeriodicalTasks(user_id)

def find_completed_tasks(user_id):
    tasks = db_manager.fetchCompletedTasks(user_id)
    tasks.sort( key=lambda x: datetime.strptime(str(x.date_completed), '%Y-%m-%d %H:%M:%S'), reverse=False)
    return list(tasks)

def find_active_tasks(user_id: int):
    return db_manager.fetchActiveTasks(user_id)

def edit_task_text_once(id, text, user_id):
    task = db_manager.find_by_id(id, user_id)
    task.task_text = text
    item = {"user_id": task.user_id, "task_text": task.task_text, "date": task.task_date, "notification": task.notification_time,
            "repeat": None, "attachments": task.attachments}
    db_manager.insert(item)
    db_manager.update_date(id, user_id)


def edit_task_text_always(id, text, user_id):
   db_manager.edit_text(id, text, user_id)

def edit_task_notification(id, notification, user_id):
    task = db_manager.find_by_id(id, user_id)
    data = {'date': task.task_date, 'notification': notification}
    date = get_notification_date(data)
    db_manager.edit_task_notification(id, date)

def delete_periodical_task(data, user_id):
    task = db_manager.find_by_id(data['task_num'], user_id)
    if data["period"] == "yes_once":
        next_date = task.task_date + timedelta(minutes=task.repeat_min)
        db_manager.update_date(data['task_num'], user_id)
        if task.notification_time != None:
            db_manager.update_notification(data['task_num'], user_id)
    if data['period'] == "no_periodicaly":
        db_manager.delete_by_id(data['task_num'], user_id)

def delete_task_files(task_id, user_id):
    task = db_manager.find_by_id(task_id, user_id)
    if task.attachments:
        file_name = task.task_text[0:20]
        file_dir = "attachments/" + str(task.user_id) + "/" + str(file_name)
        shutil.rmtree(file_dir)

def get_file_dir(task_id, user_id):
    task = db_manager.find_by_id(task_id, user_id)
    if task.attachments:
        file_dir = "attachments/" + str(task.user_id) + "/" + str(task_id)
        return file_dir
    return None

def find_task_with_attachments(task_id, user_id):
    task = db_manager.fetchAttachmentsTasks(task_id, user_id)
    if len(task) == 0:
        return None
    else:
        return task

def change_attachments_status(task_id, user_id):
    task = db_manager.change_attachments(task_id, user_id)

def check_date(date):
    pattern1 = re.compile(r'^\d{2}/\d{2}/\d{2}$')
    pattern2 = re.compile(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}$')
    if re.match(pattern1, date):
        date += ' 00:00'
    if not re.match(pattern2, date) or re.match(pattern1, date):
        return "Invalid date format.\n\n Correct formats:\n" \
                               + message_manager.emoji_date + "dd/mm/yy\n" + message_manager.emoji_date + "dd/mm/yy hh:mm\n\nIf task has no date type -"
    if int(date[:2]) > 31 or int(date[:2]) <= 0 or int(date[3:5]) > 12 or int(date[:2]) <= 0:
        return "Invelid date. Try again or type - if you task have no date"
    if len(date) > 8 and (int(date[9:11]) > 23 or int(date[12:14]) > 59 ):
        return "Invelid time. Try again or type - if you task have no date"
    datetime_object = datetime.strptime(date, '%d/%m/%y %H:%M')
    if datetime_object < datetime.now() - timedelta(days=1):
        return "You can't enter date from the past. Try again or type - if you task have no date"
    return datetime_object

def edit_date(id, new_date, user_id):
    task = db_manager.find_by_id(id, user_id)
    db_manager.edit_task_date_by_id(id, new_date)
    if task.notification_time != None and new_date == None:
        db_manager.delete_notification_by_id(id, user_id)
        db_manager.delete_repetition_by_id(id, user_id)