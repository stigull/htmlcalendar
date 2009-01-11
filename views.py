import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext


def show_calendar(request, year = None, month = None, day = None):
    now = datetime.datetime.now()
    if year is None or month is None:
        year = now.year
        month = now.month
        day = now.day
    else:
        year = int(year)
        month = int(month)
        if day is None and year == now.year and month == now.month:
            day = now.day
        else:
            day = 1

    if request.method == "GET":
        context = {'current_day': datetime.date(year, month, day) }
        return render_to_response('htmlcalendar/calendar_base.html', context, context_instance =
                                                                                RequestContext(request))
