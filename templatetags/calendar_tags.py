#coding: utf-8
import datetime

from django import template

from htmlcalendar.classes import Calendar, CalendarDay

register = template.Library()

def get_calendar(year = None, month = None):
    if year is None or month is None:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
    calendar = Calendar(year)
    return {'month': calendar.get_month(month) }
register.inclusion_tag('htmlcalendar/calendar.html')(get_calendar)

def get_events_for_month(year, month):
    calendar = Calendar(year)
    month = calendar.get_month(month)
    return {'events': month.get_events() }
register.inclusion_tag('htmlcalendar/events_for_month.html')(get_events_for_month)

def get_events_for_day(year, month,day):
    calendarday = CalendarDay(datetime.date(year, month, day), True)
    return {'events': calendarday.events }
register.inclusion_tag('htmlcalendar/events_for_day.html')(get_events_for_day)