import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Instructor, User, Reservation


def index(request):
    """
    Home page: shows instructor selector and booking form.
    GET /
    Returns: HTML page with instructor list
    """
    instructors = Instructor.objects.all()
    return render(request, 'booking/index.html', {
        'instructors': instructors,
    })


def calendar(request):
    """
    HTMX partial: returns available dates for selected instructor.
    GET /calendar/?instructor=<id>
    Returns: HTML partial with available dates
    """
    instructor_id = request.GET.get('instructor')
    if not instructor_id:
        return HttpResponse('<p>Please select an instructor.</p>')

    try:
        instructor = Instructor.objects.get(id=instructor_id)
    except Instructor.DoesNotExist:
        return HttpResponse('<p>Instructor not found.</p>', status=404)

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
    """
    Process a reservation request.
    POST /reserve/
    Body: instructor_id, date (YYYY-MM-DD), slot (1-3), name
    Returns: HTML fragment with success or error message
    """
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)

    instructor_id = request.POST.get('instructor_id', '').strip()
    date_str = request.POST.get('date', '').strip()
    slot_str = request.POST.get('slot', '').strip()
    name = request.POST.get('name', '').strip()

    if not name:
        return HttpResponse(
            '<p class="message-error">Please enter your name.</p>'
        )

    if slot_str not in ('1', '2', '3'):
        return HttpResponse(
            '<p class="message-error">Invalid time slot selected.</p>'
        )
    slot = int(slot_str)

    try:
        instructor = Instructor.objects.get(id=instructor_id)
    except Instructor.DoesNotExist:
        return HttpResponse(
            '<p class="message-error">Instructor not found.</p>', status=404
        )

    try:
        date = datetime.date.fromisoformat(date_str)
    except ValueError:
        return HttpResponse(
            '<p class="message-error">Invalid date format.</p>'
        )

    today = datetime.date.today()
    if date <= today or date > today + datetime.timedelta(days=14):
        return HttpResponse(
            '<p class="message-error">Date must be within the next 14 days.</p>'
        )

    if date.weekday() >= 5:
        return HttpResponse(
            '<p class="message-error">Weekends are not available.</p>'
        )

    already_booked = Reservation.objects.filter(
        instructor=instructor, date=date, slot=slot
    ).exists()

    if already_booked:
        return HttpResponse(
            '<p class="message-error">Sorry, that slot was just taken. '
            'Please choose another.</p>'
        )

    # NOTE: no authentication yet; name-only lookup is a placeholder
    user, _ = User.objects.get_or_create(
        name=name, defaults={'password': ''}
    )
    Reservation.objects.create(
        date=date, slot=slot, instructor=instructor, user=user
    )

    slot_names = {1: 'Morning', 2: 'Afternoon', 3: 'Evening'}
    return HttpResponse(
        f'<p class="message-success">Booked! {instructor.name} on {date}, '
        f'{slot_names[slot]} slot. See you there, {name}!</p>'
    )


def my_bookings(request):
    """
    Show booking history for a user.
    GET /my-bookings/?name=<name>
    Returns: HTML page with list of past reservations
    """
    name = request.GET.get('name', '').strip()
    if not name and request.session.get('user_name'):
        name = request.session['user_name']

    reservations = []
    if name:
        try:
            user = User.objects.get(name=name)
            reservations = Reservation.objects.filter(
                user=user
            ).order_by('-date')
        except User.DoesNotExist:
            pass

    return render(request, 'booking/my_bookings.html', {
        'reservations': reservations,
        'name': name,
    })


def register(request):
    """
    User registration page.
    GET  /register/ - show registration form
    POST /register/ - process registration
    Returns: HTML page or redirect to home
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        password = request.POST.get('password', '').strip()

        if not name:
            return render(request, 'booking/register.html', {
                'error': 'Name cannot be empty.'
            })

        if len(password) < 4:
            return render(request, 'booking/register.html', {
                'error': 'Password must be at least 4 characters.',
                'name': name,
            })

        if User.objects.filter(name=name).exists():
            return render(request, 'booking/register.html', {
                'error': 'Username already exists.',
                'name': name,
            })

        user = User.objects.create(name=name, password=password)
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        return redirect('index')

    return render(request, 'booking/register.html')


def login_view(request):
    """
    User login page.
    GET  /login/ - show login form
    POST /login/ - process login
    Returns: HTML page or redirect to home
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        password = request.POST.get('password', '').strip()

        if not name or not password:
            return render(request, 'booking/login.html', {
                'error': 'Please enter both name and password.'
            })

        try:
            user = User.objects.get(name=name, password=password)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('index')
        except User.DoesNotExist:
            return render(request, 'booking/login.html', {
                'error': 'Invalid name or password.',
                'name': name,
            })

    return render(request, 'booking/login.html')


def logout_view(request):
    """
    Logout: clear session and redirect to home.
    GET /logout/
    Returns: redirect to home page
    """
    request.session.flush()
    return redirect('index')