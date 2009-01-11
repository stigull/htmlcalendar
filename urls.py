#coding: utf-8
from django.conf.urls.defaults import *

from htmlcalendar.views import show_calendar

urlpatterns = patterns('',
      url(r'^$', show_calendar, name ='show_calendar_index'),
      url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', show_calendar, name ='show_calendar_month'),
      url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', show_calendar, name ='show_calendar_day'),
)
