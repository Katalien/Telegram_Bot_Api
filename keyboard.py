from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_btn_new_task = InlineKeyboardButton('Add new task', callback_data='new_task')
inline_btn_show_all = InlineKeyboardButton('Show tasks', callback_data='show_tasks')
inline_btn_delete_task = InlineKeyboardButton('Delete task', callback_data='delete_task')
inline_btn_edit_task = InlineKeyboardButton('Edit task', callback_data='edit_task')
inline_kb_start = InlineKeyboardMarkup(row_width=2).add(inline_btn_new_task)
inline_kb_start.add(inline_btn_show_all)
inline_kb_start.add(inline_btn_edit_task)

inline_btn_yes = InlineKeyboardButton('Yes', callback_data='yes_once')
inline_btn_no = InlineKeyboardButton('No', callback_data='no_periodicaly')
inline_kb_yes_no = InlineKeyboardMarkup(row_width=2)
inline_kb_yes_no.add(inline_btn_yes, inline_btn_no)

# menu keyboard for show different tasks
btn_show_active_tasks = KeyboardButton('Show all tasks', callback_data='active_tasks')
btn_show_completed = KeyboardButton('Show completed tasks', callback_data='completed_tasks')
btn_show_periodical = KeyboardButton('Show periodical tasks', callback_data='periodical_tasks')
btn_show_task_attachments = KeyboardButton('Show attachments', callback_data='task_with_attachment')
btn_show_back = KeyboardButton('Back to menu', callback_data='cancel_show')
kb_show = ReplyKeyboardMarkup(row_width=3).add(btn_show_active_tasks )
kb_show.add(btn_show_completed, btn_show_periodical, btn_show_task_attachments )
kb_show.add(btn_show_back)

# menu edit tasks
btn_edit_make_done = KeyboardButton('Make Done', callback_data='active_tasks')
btn_edit_date = KeyboardButton('Edit date', callback_data='periodical_tasks')
btn_edit_text = KeyboardButton('Edit description', callback_data='periodical_tasks')
btn_edit_make_periodical = KeyboardButton('Make periodical', callback_data='periodical_tasks')
btn_edit_add_notification = KeyboardButton('Edit notification', callback_data='periodical_tasks')
btn_edit_add_files = KeyboardButton('Add files', callback_data='periodical_tasks')
btn_delete_task = KeyboardButton('Delete task', callback_data='delete_task')
btn_edit_back = KeyboardButton('Back to menu', callback_data='cancel_show')
kb_edit = ReplyKeyboardMarkup(row_width=3).add(btn_edit_make_done )
kb_edit.add(btn_edit_text, btn_edit_date)
kb_edit.add(btn_edit_add_notification, btn_edit_add_files, btn_delete_task)
kb_edit.add(btn_edit_back)

#  done button
btn_done = KeyboardButton("That's all", callback_data='done')
kb_done = ReplyKeyboardMarkup(row_width=3).add(btn_done )

#  no attach button
btn_no_attach = KeyboardButton("No attach", callback_data='no attach')
kb_no_attach = ReplyKeyboardMarkup(row_width=3).add(btn_no_attach )

btn_new_task = KeyboardButton('Add new task', callback_data='new_task')
btn_show_all = KeyboardButton('Show tasks')
# btn_delete_task = KeyboardButton('Delete task', callback_data='delete_task')
btn_edit_task = KeyboardButton('Edit task', callback_data='edit_task2')
kb_start = ReplyKeyboardMarkup(row_width=2).add(inline_btn_new_task)
kb_start.add(btn_show_all)
kb_start.add(btn_edit_task)

inline_kb_task_editing = InlineKeyboardMarkup().add(inline_btn_delete_task).add(inline_btn_edit_task)

inline_btn_edit_text = InlineKeyboardButton('Task text', callback_data='edit_task_text')
inline_btn_edit_date = InlineKeyboardButton('Date', callback_data='edit_task_date')
inline_btn_edit_repeat = InlineKeyboardButton('Repeat', callback_data='btn_edit_frq')

inline_kb_edit2 = InlineKeyboardMarkup(row_width=2).add(inline_btn_edit_text,
                                                        inline_btn_edit_date,
                                                        inline_btn_edit_repeat
                                                        )

inline_kb_repeat_hour = InlineKeyboardButton('Hour', callback_data='hour')
inline_kb_repeat_day = InlineKeyboardButton('Day', callback_data='day')
inline_kb_repeat_week = InlineKeyboardButton('Week', callback_data='week')
inline_kb_repeat_month = InlineKeyboardButton('Month', callback_data='month')
inline_kb_repeat_no_repeat = InlineKeyboardButton("don't repeat", callback_data='no_repeat')
repeat_kb = InlineKeyboardMarkup().add(inline_kb_repeat_hour, inline_kb_repeat_day,
                                       inline_kb_repeat_week, inline_kb_repeat_month,
                                       inline_kb_repeat_no_repeat)

inline_kb_notify_1 = InlineKeyboardButton('10 minutes', callback_data='10 minutes')
inline_kb_notify_2 = InlineKeyboardButton('30 minutes', callback_data='30 minutes')
inline_kb_notify_3 = InlineKeyboardButton('1 hour', callback_data='1 hour')
inline_kb_notify_4 = InlineKeyboardButton('1 day', callback_data='1 day')
inline_kb_notify_no = InlineKeyboardButton("don't remind", callback_data='no notify')
notification_kb = InlineKeyboardMarkup().add(inline_kb_notify_1 , inline_kb_notify_2,
                                       inline_kb_notify_3, inline_kb_notify_4,
                                       inline_kb_notify_no)

inline_btm_return_to_active = InlineKeyboardButton('return task to active', callback_data='return_to_active')
inline_kb_return = InlineKeyboardMarkup().add(inline_btm_return_to_active)