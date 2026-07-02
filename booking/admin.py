from django.contrib import admin
from .models import Instructor, User, Reservation

admin.site.register(Instructor)
admin.site.register(User)
admin.site.register(Reservation)