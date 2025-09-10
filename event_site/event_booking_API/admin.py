from django.contrib import admin
from .models import Event, Attendee, Booking, Speaker, Session
from django.utils.html import format_html

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'location', 'total_seats', 'available_seats', 'ticket_price', 'image_preview', 'get_sessions_info']
    list_filter = ['event_date', 'location']
    search_fields = ['event_name', 'location']
    readonly_fields = ['available_seats']
    fieldsets = (
        ('Event Details', {
            'fields': ('event_name', 'event_date', 'location', 'total_seats', 'available_seats', 'ticket_price'),
        }),
        ('Image', {
            'fields': ('image',),
            'description': 'Upload an optional image for the event.',
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image Preview'

    def get_sessions_info(self, obj):
        sessions = Session.objects.filter(event=obj)
        if sessions.exists():
            return ', '.join([f"{s.session_title} by {s.speaker.first_name} {s.speaker.last_name}" for s in sessions])
        return 'No sessions scheduled'
    get_sessions_info.short_description = 'Sessions Overview'

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user_email', 'phone', 'get_bookings_count']
    search_fields = ['first_name', 'last_name', 'user__email', 'phone']
    readonly_fields = ['user', 'first_name', 'last_name', 'phone']
    fieldsets = (
        ('User Association', {
            'fields': ('user',),
            'description': 'This Attendee is automatically created based on the User who registers or books an event.',
        }),
        ('Details (Auto-populated)', {
            'fields': ('first_name', 'last_name', 'phone'),
            'description': 'These fields are populated from the associated User model upon creation.',
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def get_bookings_count(self, obj):
        return Booking.objects.filter(attendee=obj).count()
    get_bookings_count.short_description = 'Bookings Count'

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['attendee_names', 'event_name', 'seats_booked', 'amount_paid', 'booking_date']
    list_filter = ['booking_date', 'event']
    search_fields = ['attendee__first_name', 'attendee__last_name', 'event__event_name']
    readonly_fields = ['amount_paid', 'booking_date', 'attendee', 'event']

    def attendee_names(self, obj):
        return f"{obj.attendee.first_name} {obj.attendee.last_name} ({obj.attendee.user.email})"
    attendee_names.short_description = 'Attendee'

    def event_name(self, obj):
        return obj.event.event_name
    event_name.short_description = 'Event'
    event_name.admin_order_field = 'event__event_name'

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'topic']
    search_fields = ['first_name', 'last_name', 'topic']

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