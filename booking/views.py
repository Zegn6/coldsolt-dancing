from django.shortcuts import render
from django.http import HttpResponse
from .models import Instructor, User, Reservation
import datetime

def index(request):
    instructors = Instructor.objects.all()
    return render(request, 'booking/index.html', {
        'instructors': instructors,
    })

def calendar(request):
    instructor_id = request.GET.get('instructor')
    if not instructor_id:
        return HttpResponse('<p>Please select an instructor.</p>')

    instructor = Instructor.objects.get(id=instructor_id)
    today = datetime.date.today()
    dates = []

    for i in range(1, 15):
        date = today + datetime.timedelta(days=i)
        if date.weekday() >= 5:
            continue
        booked = Reservation.objects.filter(
            instructor=instructor, date=date
        ).count()
        if booked < 3:
            dates.append(date)

    return render(request, 'booking/calendar.html', {
        'instructor': instructor,
        'dates': dates,
    })

def reserve(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)

    instructor_id = request.POST.get('instructor_id')
    date_str = request.POST.get('date')
    slot = int(request.POST.get('slot'))
    name = request.POST.get('name')

    instructor = Instructor.objects.get(id=instructor_id)
    date = datetime.date.fromisoformat(date_str)

    # Check if slot is already taken
    already_booked = Reservation.objects.filter(
        instructor=instructor, date=date, slot=slot
    ).exists()

    if already_booked:
        return HttpResponse(
            '<p style="color:red;">Sorry, that slot was just taken. Please choose another.</p>'
        )

    # Get or create user by name
    user, _ = User.objects.get_or_create(name=name, defaults={'password': ''})

    # Create reservation
    Reservation.objects.create(
        date=date, slot=slot, instructor=instructor, user=user
    )

    slot_names = {1: 'Morning', 2: 'Afternoon', 3: 'Evening'}
    return HttpResponse(
        f'<p style="color:green;">Booked! {instructor.name} on {date}, '
        f'{slot_names[slot]} slot. See you there, {name}!</p>'
    )