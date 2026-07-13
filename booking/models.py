from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # NOTE: should use hashing in production

    def __str__(self):
        return self.name


class Reservation(models.Model):
    SLOT_CHOICES = [
        (1, 'Morning'),
        (2, 'Afternoon'),
        (3, 'Evening'),
    ]

    date = models.DateField()
    slot = models.IntegerField(choices=SLOT_CHOICES)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('instructor', 'date', 'slot')

    def __str__(self):
        slot_names = {1: 'Morning', 2: 'Afternoon', 3: 'Evening'}
        return (
            f"{self.date} {slot_names.get(self.slot, self.slot)}"
            f" - {self.instructor.name} ({self.user.name})"
        )