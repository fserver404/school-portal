from django.contrib import admin

# Register your models here.
from .models import User, Subject, Grade, Announcement, CalendarEvent

admin.site.register(Announcement)
admin.site.register(CalendarEvent)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role", "email")
    list_filter = ("role",)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "score", "date")
    list_filter = ("subject", "date")
