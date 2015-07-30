# -*- coding: utf-8 -*-

import calendar
import datetime

import django.db.models as models
from django.core.urlresolvers import reverse

from utils.dateformatting import MONTHS

JANUARY = 1
DECEMBER = 12

class CalendarEventManager(object):
    def __init__(self):
        self.event_callbacks = []

    def register_callback(self, callback):
        """
        Pre:    callback is a function who takes one argument called date
                and returns a list of CalendarEvent instances
        Post:   callback has been added to the callback registry
        """
        self.event_callbacks.append(callback)

    def get_events_for(self, date):
        events = []
        for callback in self.event_callbacks:
            events_to_add = callback(date)
            if events_to_add is not None:
                events.extend(events_to_add)
        return events

event_manager = CalendarEventManager()


class CalendarDay(object):
    def __init__(self, date, is_current_month):
        self.is_current_month = is_current_month
        self.date = date
        if date.year >= 1900:
            self.events = event_manager.get_events_for(date)
        else:
            self.events = []

    def is_in_current_month(self):
        return self.is_current_month

    def has_events(self):
        return len(self.events) > 0

    def get_css_classes(self):
        now = datetime.date.today()
        css_classes = []
        if not self.is_current_month:
            css_classes.append("other-month")
        if self.date < now:
            css_classes.append("in-the-past")
        if self.date == now:
            css_classes.append("today")

        return " ".join(css_classes)

    def get_event_titles(self):
        return "; ".join(["%s: %s" % (event.event_type, event.name) for event in self.events ])

    def get_absolute_url(self):
        return ('show_calendar_day', (), { 'year': self.date.strftime("%Y"),
                                            'month': self.date.strftime("%m"),
                                            'day': self.date.strftime("%d"),
                                            })
    get_absolute_url = models.permalink(get_absolute_url)



    def __unicode__(self):
        return "%d" % self.date.day

class CalendarEvent(object):
    def __init__(self, event_type, name, url, description = ""):
        self.event_type = event_type
        self.name = name
        self.url = url
        self.description = description


class CalendarWeek(object):
    def __init__(self, days, current_month):
        self.current_month = current_month
        self.days = days

    def __iter__(self):
        return self

    def next(self):
        try:
            day = self.days.pop(0)
            return CalendarDay(day, day.month == self.current_month)
        except IndexError:
            raise StopIteration()


class CalendarMonth(object):

    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.date = datetime.date(year, month, 1)
        self.name = MONTHS[month].title()

        cal = calendar.Calendar(calendar.SUNDAY)
        self.weeks = cal.monthdatescalendar(year, month)


    def get_weekdaynames(self):
        return [u"Sun", u"Mán", u"Þri", u"Mið", u"Fim", u"Fös", u"Lau"]

    def __iter__(self):
        return self

    def next(self):
        try:
            days = self.weeks.pop(0)
            return CalendarWeek(days, self.month)
        except IndexError:
            raise StopIteration()

    def get_absolute_url(self):
        return ('show_calendar_month', (), { 'year': self.date.strftime("%Y"),
                                            'month': self.date.strftime("%m"),
                                            })
    get_absolute_url = models.permalink(get_absolute_url)

    def get_events(self):
        events = []
        for week in self.weeks:
            for day in week:
                if day.month == self.month:
                    calendar_day = CalendarDay(day, True)
                    if calendar_day.has_events():
                        events.append((day, calendar_day.events))
        return events

    def get_last_month_url(self):
        if self.month == JANUARY:
            year = self.year - 1
            month = 12
        else:
            year = self.year
            month = self.month -1
            
        if year < 1900:
            return None
        else:
            last_month = datetime.date(year, month, 1)
            return self._get_month_url(last_month)

    def get_next_month_url(self):
        if self.month == DECEMBER:
            year = self.year + 1
            month = 1
        else:
            year = self.year
            month = self.month + 1

        next_month = datetime.date(year, month, 1)
        return self._get_month_url(next_month)

    def _get_month_url(self, date):
        return reverse('show_calendar_month', kwargs = {'year': date.strftime("%Y"),
                                                        'month': date.strftime("%m") })

class Calendar(object):

    def __init__(self, year):
        self.year = year

    def get_month(self, month):
        return CalendarMonth(self.year, month)

