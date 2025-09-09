from django.contrib import admin
from .models import Event, Attendee, Booking, Speaker, Session

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'location', 'total_seats', 'available_seats', 'ticket_price', 'get_sessions_info']
    list_filter = ['event_date', 'location']
    search_fields = ['event_name', 'location']
    readonly_fields = ['available_seats']  
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Details', {
            'fields': ('event_name', 'event_date', 'location', 'total_seats', 'available_seats', 'ticket_price'),
            'description': 'Core information for the event. Available seats are automatically updated upon booking and cannot be edited manually.',
        }),
    )
    
    def get_attendees(self, obj):
        """
        Custom method to display a comma-separated list of attendee names for the event.
        """
        attendees = Attendee.objects.filter(booking__event=obj).distinct()
        if attendees.exists():
            return ', '.join([f"{a.first_name} {a.last_name} ({a.user.email})" for a in attendees])
        return 'No attendees yet'
    get_attendees.short_description = 'Attendees'
    
    def get_sessions_info(self, obj):
        """
        Custom method to summarize associated sessions and speakers.
        """
        sessions = Session.objects.filter(event=obj)
        if sessions.exists():
            return ', '.join([f"{s.session_title} by {s.speaker.first_name} {s.speaker.last_name}" for s in sessions])
        return 'No sessions scheduled'
    get_sessions_info.short_description = 'Sessions Overview'

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user_email', 'phone']
    list_filter = ['phone']
    search_fields = ['first_name', 'last_name', 'user__email', 'phone']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'topic']
    search_fields = ['first_name', 'last_name', 'topic']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['attendee_names', 'event_name', 'seats_booked', 'amount_paid', 'booking_date']
    list_filter = ['booking_date', 'event']
    search_fields = ['attendee__first_name', 'attendee__last_name', 'event__event_name']
    readonly_fields = ['amount_paid', 'booking_date']
    
    def attendee_names(self, obj):
        return f"{obj.attendee.first_name} {obj.attendee.last_name} ({obj.attendee.user.email})"
    attendee_names.short_description = 'Attendee'
    
    def event_name(self, obj):
        return obj.event.event_name
    event_name.short_description = 'Event'
    event_name.admin_order_field = 'event__event_name'

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_title', 'speaker_names', 'start_time', 'end_time', 'event_name']
    list_filter = ['start_time', 'end_time', 'event']
    search_fields = ['session_title', 'speaker__first_name', 'speaker__last_name']
    
    def speaker_names(self, obj):
        return f"{obj.speaker.first_name} {obj.speaker.last_name}"
    speaker_names.short_description = 'Speaker'
    
    def event_name(self, obj):
        return obj.event.event_name
    event_name.short_description = 'Event'
    event_name.admin_order_field = 'event__event_name'