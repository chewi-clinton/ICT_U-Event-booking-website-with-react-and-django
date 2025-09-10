from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from .models import Attendee, Event, Booking
from .serializers import UserSerializer, EventSerializer, BookingSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        attendee, created = Attendee.objects.get_or_create(
            user=self.request.user,
            defaults={
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "phone": getattr(self.request.user, "profile_phone", "")
            }
        )
        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=self.request.data["event"])
            if event.available_seats < serializer.validated_data["seats_booked"]:
                raise ValueError("Not enough seats available.")
            event.available_seats -= serializer.validated_data["seats_booked"]
            event.save()
        serializer.save(attendee=attendee, amount_paid=serializer.validated_data["seats_booked"] * event.ticket_price)

class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]