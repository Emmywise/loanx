from django.shortcuts import render
import datetime
import calendar
from django.utils import timezone
from django.db.models import Q
from fine_search.fine_search import perform_search_queryset
from rest_framework.viewsets import ModelViewSet
from .models import CalendarEventEmail, CalendarEvent, CalendarLog
from .serializers import CalendarEventEmailSerializer, CalendarEventSerializer, CalendarLogSerializer
# Create your views here.


def filter_date(request, queryset):
    view = request.GET.get('view')
    date = request.GET.get('date')
    if date:
        date_split = date.split('-')
        date_split = list(map(int, date_split))
        current_date_lower = datetime.datetime(date_split[0], date_split[1], date_split[2],
                                               tzinfo=timezone.utc)
        current_date_upper = datetime.datetime(date_split[0], date_split[1], date_split[2],
                                               23, 59, 59,
                                               tzinfo=timezone.utc)
        lower_date_week = current_date_lower + datetime.timedelta(days=-current_date_lower.weekday())
        upper_date_week = current_date_upper + datetime.timedelta(days=6 - current_date_upper.weekday())
        lower_date_month = datetime.datetime(date_split[0], date_split[1], 1, tzinfo=timezone.utc)
        upper_date_month = datetime.datetime(date_split[0], date_split[1],
                                             calendar.monthrange(date_split[0], date_split[1])[1], tzinfo=timezone.utc)

        if view and (view == 'daily'):
            queryset = queryset.filter(
                Q(date__day=current_date_lower.day) &
                Q(date__month=current_date_lower.month) &
                Q(date__year=current_date_lower.year)
            )

        if view and (view == 'weekly'):
            queryset = queryset.filter(
                Q(date__gte=lower_date_week) &
                Q(date__lte=upper_date_week)
            )
        if view and (view == 'monthly'):
            queryset = queryset.filter(
                Q(date__gte=lower_date_month) &
                Q(date__lte=upper_date_month)
            )

    return queryset


class CalenderEventEmailViewSet(ModelViewSet):
    serializer_class = CalendarEventEmailSerializer

    def get_queryset(self):
        queryset = CalendarEventEmail.objects.all()
        if self.request.GET.get('calendar_event'):
            queryset = queryset.filter(
                calendar__pk=self.request.GET.get('calendar_event')
            )
        return queryset


class CalendarEventViewSet(ModelViewSet):
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        queryset = CalendarEvent.objects.all()

        branch = self.request.GET.get('branch')
        date_from = self.request.GET.get('date_from')
        till_date = self.request.GET.get('till_date')
        q = self.request.GET.get('q')

        if branch:
            queryset = queryset.filter(branch__pk=branch)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if till_date:
            queryset = queryset.filter(till_date__lte=till_date)
        queryset = filter_date(self.request, queryset)
        if q:
            queryset = perform_search_queryset(queryset, q, ['title', 'description'])
        return queryset


class CalendarLogViewSet(ModelViewSet):
    serializer_class = CalendarLogSerializer

    def get_queryset(self):
        queryset = CalendarLog.objects.all()
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__pk=branch)
        queryset = filter_date(self.request, queryset)
        return queryset
