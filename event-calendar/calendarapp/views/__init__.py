from .event_list import AllEventsListView, CompletedEventsListView, RunningEventsListView, UpcomingEventsListView
from .other_views import (
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
    delete_event,
    next_week,
    next_day,
add_shift_request,api_shift_types_with_deficit


)
from .views import (timetable,instance_list,instance_detail,choose_instance,select_instance,choose_shift_requests,choose_dayoff_requests,requests_submitted,DashboardView,confirm_schedule,cancel_schedule,schedule_log_events,unit_details_ajax,choose_emergency_requests)
from .views_chat import(
    ChatView,
    chat_bubble,
    shift_table_fragment,)
from .views_scheduler import (SchedulerView,debug_box)

__all__ = {
    AllEventsListView,
    RunningEventsListView,
    UpcomingEventsListView,
    CompletedEventsListView,
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
    delete_event,
    next_week,
    next_day,
    ChatView, chat_bubble, shift_table_fragment,

}


