from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User

# users and roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.username} ({self.role})"


# subjects
class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "teacher"},
        related_name="subjects"
    )
    students = models.ManyToManyField(
        User,
        related_name="enrolled_subjects",
        blank=True,
        limit_choices_to={"role": "student"}
    )

    def __str__(self):
        return self.name


# score
class Grade(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        related_name="grades"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="grades")
    score = models.FloatField()
    date = jmodels.jDateField()

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}: {self.score}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} - {self.date}"