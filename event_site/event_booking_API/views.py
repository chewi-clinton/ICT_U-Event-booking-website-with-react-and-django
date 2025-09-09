from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Attendee, Event, Booking
from .serializers import AttendeeSerializer, EventSerializer, BookingSerializer
from rest_framework.permissions import IsAdminUser

class RegisterView(generics.CreateAPIView):
    serializer_class = AttendeeSerializer

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
    def perform_create(self, serializer):
        attendee = Attendee.objects.get(user=self.request.user)
        serializer.save(attendee=attendee)

class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()