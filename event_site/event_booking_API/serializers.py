from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Booking, Attendee

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        user = User.objects.create_user(**validated_data)
        Attendee.objects.create(
            user=user,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=phone
        )
        return user

class EventSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['event', 'seats_booked']