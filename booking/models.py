from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    date = models.DateField()
    slot = models.IntegerField()  # 1, 2, 3 (session of the day)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} slot{self.slot} - {self.instructor.name}"