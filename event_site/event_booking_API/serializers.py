from rest_framework import serializers
from .models import Attendee, Event, Booking
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AttendeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Attendee
        fields = ['user', 'first_name', 'last_name', 'phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        attendee = Attendee.objects.create(user=user, **validated_data)
        return attendee

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'