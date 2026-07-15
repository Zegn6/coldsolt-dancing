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
            'password': 'testpass',
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