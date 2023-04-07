# import asyncio
# from bot import bot
# import db_manager
# import message_manager
# import aioschedule
# from datetime import *
#
# # def notify(date: str):
# #     all_tasks = db_manager.find_by_date(date)
# #     local_time = datetime.now()[:-9] + "00"
# #     print(datetime.now().timestamp())
# #     print(datetime.now())
# #     if len(all_tasks) != 0:
# #         for task in all_tasks:
# #             message = message_manager.all_tasks_message(task)
# #             await bot.send_message(chat_id=task['user_id'], text=message)
# #             if task.repeat_min is not:
# #                 new_notification = local_time + timedelta(minutes=task.period)
# #                 db_manager.edit_task_notification(id, new_notification)
#
#
# def send_tasks():
#     aioschedule.every(58).seconds.do(notify)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)