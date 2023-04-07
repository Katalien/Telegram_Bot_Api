def all_tasks_message(tasks):
    message = 'YOUR TASKS: \n\n'
    counter = 1
    for task in tasks:
        message += str(task.id) + ") "
        message += task.task_text + "\n"
        if task.task_date != None:
            message += "Date: " + str(task.task_date)
        if task.notification_time != None:
            cur_str = make_notification_from_task(task)
            if cur_str != '':
                message += "\nNotify in " + cur_str
        if task.repeat_min != None:
            message += "\ntask is repeatable"
        if task.attachments == True:
            message += "\ntask with attachments"
        message += '\n\n'
        counter += 1
    message += "\nAmount: " + str(len(tasks))
    return message

def mes_from_task(task):
    message = 'Reminder: \n\n'
    message += str(task.id) + ") "
    message += task.task_text + "\n"
    if task.task_date != None:
        message += "Date: " + str(task.task_date)
    if task.notification_time != None:
        message += "\nNotify in " + make_notification_from_task(task)
    if task.repeat_min != None:
        message += "\ntask is repeatable"
    message += '\n\n'
    return message

def make_notification_from_task(task):
    date = task.task_date
    notification = task.notification_time
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



