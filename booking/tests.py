import datetime

from django.test import TestCase

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
        """slot=1のとき'Morning'が表示されるか"""
        self.assertIn("Morning", str(self.reservation))