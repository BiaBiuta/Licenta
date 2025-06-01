from django.contrib import admin
from calendarapp import models
from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
# Dez‐înregistrăm modelul Group
admin.site.unregister(Group)

# Dacă vrei să ascunzi și permisiunile din meniul Admin

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    change_list_template = "admin/calendarapp/event/change_list.html"

    model = models.Event
    list_display = [
        "id",
        "title",
        "user",
        "is_active",
        "is_deleted",
        "is_approved",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted", "is_approved","department_id"]
    search_fields = ["title"]
    actions = ["approve_events"]

    def get_queryset(self, request):
        """Show only unapproved events to the admin by default."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(is_approved=False)
        return qs

    def approve_events(self, request, queryset):
        """Approve selected events."""
        queryset.update(is_approved=True)
        self.message_user(request, "Selected events have been approved.")
    approve_events.short_description = "Approve selected events"


@admin.register(models.EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = models.EventMember
    list_display = ["id", "event", "user", "created_at", "updated_at"]
    list_filter = ["event"]
# from django.contrib import admin
# from models.nurse import Nurse
#
# @admin.register(Nurse)
# class NurseAdmin(admin.ModelAdmin):
#     list_display = ('user', 'employee_id', 'max_shifts')
from django.contrib import admin
from calendarapp.models.coverage_requirements import CoverageRequirement

@admin.register(CoverageRequirement)
class CoverageRequirementAdmin(admin.ModelAdmin):
    list_display  = ('day', 'shift_id', 'requirement', 'weight_under', 'weight_over', 'department')
    list_editable = ('requirement', 'weight_under', 'weight_over')
    list_per_page = 14   # vezi câte zile ai
    ordering      = ('day',)
from django.contrib import admin


# admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from calendarapp.models.day_shift_type import DayShiftType
from calendarapp.models.global_object import GlobalObject
from calendarapp.models.cereri.shift_request import ShiftRequest
from calendarapp.models.cereri.dayoff_request import DayOffRequest

class GlobalObjectFilter(admin.SimpleListFilter):
    title = _('Global Object')
    parameter_name = 'global_object'

    def lookups(self, request, model_admin):
        return [
            (go.id, f"{go.id} – Department")
            for go in GlobalObject.objects.all()
        ]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Day__GlobalObject_id=self.value())
        return queryset

@admin.register(DayShiftType)
class DayShiftTypeAdmin(admin.ModelAdmin):
    list_display  = ('Day', 'ShiftType', 'NrRequired', 'UnderCoverWeight', 'OverCoverWeight')
    list_editable = ('NrRequired', 'UnderCoverWeight', 'OverCoverWeight')
    list_filter   = (GlobalObjectFilter, )
    ordering      = ('Day__DayID', 'ShiftType__ShiftID')

@admin.register(ShiftRequest)
class ShiftRequestAdmin(admin.ModelAdmin):
    list_display = ('nurse','department','day','shift_type','req_type','weight','status')
    list_editable = ('status',)
    list_filter  = ('department','status','req_type')
    actions      = ('approve_requests','deny_requests',)

    @admin.action(description="Approve selected")
    def approve_requests(self, request, queryset):
        updated = queryset.filter(status='P').update(status='A')
        self.message_user(request, f"{updated} cereri aprobate.")

    @admin.action(description="Deny selected")
    def deny_requests(self, request, queryset):
        updated = queryset.filter(status='P').update(status='D')
        self.message_user(request, f"{updated} cereri respinse.")
@admin.register(DayOffRequest)
class DayOffRequestAdmin(admin.ModelAdmin):
    list_display  = ('nurse','department','day','status','from_file')
    list_editable = ('status',)
    list_filter   = ('department','status','from_file')
    actions       = ('approve','deny',)

    @admin.action(description="Approve selected")
    def approve(self, request, qs):
        cnt = qs.filter(status='P', from_file=True).update(status='A')
        self.message_user(request, f"{cnt} requests approved.")
    @admin.action(description="Deny selected")
    def deny(self, request, qs):
        cnt = qs.filter(status='P').update(status='D')
        self.message_user(request, f"{cnt} requests denied.")
