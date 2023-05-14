from django import template
import datetime

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i].created_at

@register.filter
def deadline(date_task):
    if (date_task.replace(tzinfo=None) - datetime.datetime.now()) < datetime.timedelta(hours=10):
        return 1
    elif (date_task.replace(tzinfo=None) - datetime.datetime.now()) < datetime.timedelta(days=2):
        return 2
    else:
        return 3
