import datetime
import re
from typing import List, NamedTuple, Optional
from peewee import *
import datetime

db = SqliteDatabase('db/database.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db

class Task(BaseModel):
    id = PrimaryKeyField(unique=True)
    task_text = CharField(null=False)
    task_date = DateTimeField(null=True)
    notification_time = DateTimeField(null=True)
    user_id = IntegerField(null=False)
    completed = BooleanField(default=False, null=True)
    repeat_min = IntegerField(null=True)  # in minutes
    date_completed = DateTimeField(null=True)
    attachments = BooleanField(default=False)

    class Meta:
        db_table = 'tasks'
