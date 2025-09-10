from django.urls import path
from .views import RegisterView, CustomAuthToken, EventListView, BookingCreateView, EventCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('book/', BookingCreateView.as_view(), name='book'),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
]