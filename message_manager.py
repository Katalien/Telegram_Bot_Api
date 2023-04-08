emoji_done = '✅'
emoji_notify = '🔔'
emoji_repeat = '♻'
emoji_attachments = '📝'
emoji_date = '📅'

def all_tasks_message(tasks):
    message = 'YOUR TASKS: \n\n'
    counter = 1
    for task in tasks:
        message += str(task.id) + ") "
        message += task.task_text
        if task.task_date != None:
            message += "\n\n" + emoji_date + str(task.task_date)
        if task.notification_time != None:
            cur_str = make_mes_notification_from_task(task)
            if cur_str != '':
                message += "\n"+ emoji_notify + cur_str
        if task.repeat_min != None:
            #message += "\ntask is repeatable"
            message += "\n" + emoji_repeat + make_repeat_from_min(task)
        if task.attachments == True:
            # message += "\ntask with attachments"
            message += "\n" + emoji_attachments
        message += '\n\n'
        counter += 1
    message += "\nAmount: " + str(len(tasks))
    return message

def mes_from_task(task):
    message = 'Reminder: \n\n'
    message += str(task.id) + ") "
    message += task.task_text + "\n\n"
    if task.task_date != None:
        message += emoji_date + str(task.task_date)
    if task.notification_time != None:
        message += "\n" + emoji_notify + make_mes_notification_from_task(task)
    if task.repeat_min != None:
        message += "\n" + emoji_repeat + make_repeat_from_min(task)
    if task.attachments:
        message += "\n" + emoji_attachments
    message += '\n\n'
    return message

def make_mes_notification_from_task(task):
    date = task.task_date
    notification = task.notification_time
    if date == None or notification == None:
        return ""
    delta = str(date - notification)
    if delta == "0:10:00":
        return "10 minutes"
    if delta == "0:30:00":
        return "30 minutes"
    if delta == "1:00:00":
        return "1 hour"
    if delta == "1 day, 0:00:00":
        return "1 day"
    else:
        return ""

def make_repeat_from_min(task):
    repeat_min = task.repeat_min
    if repeat_min == None:
        return ""
    # less than day
    if repeat_min < 1440:
        return str(int(repeat_min / 60)) + " hours"
    # less than week
    if repeat_min < 10080:
        return str(int(repeat_min / 1440)) + " days"
    # less than month
    if repeat_min < 44640:
        return str(int(repeat_min / 10080)) + " weeks"
    # more than month
    else:
        return str(int(repeat_min / 44640)) + " months"


