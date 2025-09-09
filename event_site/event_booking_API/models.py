from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Attendee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        if self.user.password and not self.user.password.startswith('pbkdf2_'):
            self.user.password = make_password(self.user.password)
        super().save(*args, **kwargs)

class Speaker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField(default=0) 
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)
class Booking(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.event.available_seats -= self.seats_booked
        self.event.save()
        super().save(*args, **kwargs)

class Session(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    session_title = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()