from django.urls import path
from .views import RegisterView, CustomAuthToken, EventListView, BookingCreateView, EventCreateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('events/', EventListView.as_view()),
    path('book/', BookingCreateView.as_view()),
    path('events/create/', EventCreateView.as_view()),
]