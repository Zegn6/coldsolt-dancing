from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('reserve/', views.reserve, name='reserve'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
]