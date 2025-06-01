from datetime import datetime
from django.db import models
from django.urls import reverse

from calendarapp.models import EventAbstract
from accounts.models import User
from calendarapp.models.global_object  import GlobalObject

class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events
    def get_all_events_from_department(self, department):
        events = Event.objects.filter( is_active=True, is_deleted=False,department=department)
        return events


    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,

        ).order_by("start_time")
        return running_events
    def get_all_running_events(self):
        running_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
            start_time__lte = datetime.now().date(),

        ).order_by("start_time")
        return running_events

    def get_all_running_events_from_department(self,global_id):
        running_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
            start_time__lte=datetime.now().date(),
            department=global_id
        ).order_by("start_time")
        return running_events
    
    def get_completed_events(self, user):
        completed_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__lt=datetime.now().date(),
        )
        return completed_events
    def get_all_completed_events(self):
        completed_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__lt=datetime.now().date(),
        )
        return completed_events

    def get_all_completed_events_from_department(self,global_id):
        completed_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__lt=datetime.now().date(),
            department=global_id
        )
        return completed_events
    
    def get_upcoming_events(self, user):
        upcoming_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            start_time__gt=datetime.now().date(),
        )
        return upcoming_events
    def get_all_upcoming_events(self):
        upcoming_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            start_time__gt=datetime.now().date(),
        )
        return upcoming_events
    def get_all_upcoming_events_from_department(self,global_id):
        upcoming_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            start_time__gt=datetime.now().date(),
            department=global_id
        )
        return upcoming_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_approved = models.BooleanField(default=False)
    department= models.ForeignKey(GlobalObject, on_delete=models.CASCADE,default="",related_name="events")
    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
