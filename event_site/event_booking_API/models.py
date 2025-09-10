from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Attendee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Speaker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.topic}"

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField(default=0)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to='event_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

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

    def __str__(self):
        return f"{self.attendee} - {self.event}"

class Session(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    session_title = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.session_title