import datetime

from django.test import TestCase, Client
from django.urls import reverse

from .models import Instructor, User, Reservation


class InstructorModelTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(name="Anna Smith")

    def test_str(self):
        self.assertEqual(str(self.instructor), "Anna Smith")


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="John Doe", password="pass")

    def test_str(self):
        self.assertEqual(str(self.user), "John Doe")


class ReservationModelTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(name="Anna Smith")
        self.user = User.objects.create(name="John Doe", password="pass")
        self.reservation = Reservation.objects.create(
            date=datetime.date(2026, 7, 7),
            slot=1,
            instructor=self.instructor,
            user=self.user,
        )

    def test_str(self):
        self.assertIn("Anna Smith", str(self.reservation))
        self.assertIn("John Doe", str(self.reservation))

    def test_slot_value(self):
        self.assertEqual(self.reservation.slot, 1)

    def test_date(self):
        self.assertEqual(self.reservation.date, datetime.date(2026, 7, 7))

    def test_reservation_str_shows_morning(self):
        self.assertIn("Morning", str(self.reservation))


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Instructor.objects.create(name="Anna Smith")

    def test_index_returns_200(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_shows_instructors(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Anna Smith")


class CalendarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor = Instructor.objects.create(name="Anna Smith")

    def test_calendar_without_instructor(self):
        response = self.client.get(reverse('calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select an instructor")

    def test_calendar_with_instructor(self):
        response = self.client.get(
            reverse('calendar'),
            {'instructor': self.instructor.id}
        )
        self.assertEqual(response.status_code, 200)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page_returns_200(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        response = self.client.post(reverse('register'), {
            'name': 'testuser',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(name='testuser').exists())


class MyBookingsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor = Instructor.objects.create(name="Anna Smith")
        self.user = User.objects.create(name="John Doe", password="pass")
        Reservation.objects.create(
            date=datetime.date(2026, 7, 7),
            slot=1,
            instructor=self.instructor,
            user=self.user,
        )

    def test_my_bookings_shows_reservations(self):
        response = self.client.get(
            reverse('my_bookings'), {'name': 'John Doe'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anna Smith")


class ReserveViewValidationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor = Instructor.objects.create(name="Anna Smith")

    def test_reserve_empty_name(self):
        today = datetime.date.today()
        date = today + datetime.timedelta(days=1)
        if date.weekday() >= 5:
            date = today + datetime.timedelta(days=3)
        response = self.client.post(reverse('reserve'), {
            'instructor_id': self.instructor.id,
            'date': date.strftime('%Y-%m-%d'),
            'slot': '1',
            'name': '',
        })
        self.assertContains(response, 'Please enter your name')

    def test_reserve_invalid_slot(self):
        today = datetime.date.today()
        date = today + datetime.timedelta(days=1)
        response = self.client.post(reverse('reserve'), {
            'instructor_id': self.instructor.id,
            'date': date.strftime('%Y-%m-%d'),
            'slot': '9',
            'name': 'John',
        })
        self.assertContains(response, 'Invalid time slot')


class RegisterViewValidationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_empty_name(self):
        response = self.client.post(reverse('register'), {
            'name': '',
            'password': 'pass1234',
        })
        self.assertContains(response, 'Name cannot be empty')

    def test_register_short_password(self):
        response = self.client.post(reverse('register'), {
            'name': 'testuser',
            'password': 'ab',
        })
        self.assertContains(response, 'at least 4 characters')

    def test_register_duplicate_name(self):
        User.objects.create(name='existing', password='pass')
        response = self.client.post(reverse('register'), {
            'name': 'existing',
            'password': 'pass1234',
        })
        self.assertContains(response, 'already exists')


class LoginViewValidationTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create(name='testuser', password='pass1234')

    def test_login_empty_fields(self):
        response = self.client.post(reverse('login'), {
            'name': '',
            'password': '',
        })
        self.assertContains(response, 'Please enter both')

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'name': 'testuser',
            'password': 'wrongpass',
        })
        self.assertContains(response, 'Invalid name or password')

    def test_login_success_sets_session(self):
        response = self.client.post(reverse('login'), {
            'name': 'testuser',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['user_name'], 'testuser')