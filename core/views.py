import json
import jdatetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement, CalendarEvent, Subject
from django.core.serializers.json import DjangoJSONEncoder
from .models import CalendarEvent

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    return render(request, "core/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    announcements = Announcement.objects.all()[:5]
    calendar_events = CalendarEvent.objects.all().order_by('date')[:10]

    announcements = Announcement.objects.all()[:5]
    calendar_events = CalendarEvent.objects.all().order_by("date")

    # خروجی برای JS
    calendar_events_json = json.dumps(
        [{"date": e.date.strftime("%Y-%m-%d"), "title": e.title} for e in calendar_events],
        cls=DjangoJSONEncoder
    )

    context = {
        "username": request.user.username,
        "role": request.user.role,
        "announcements": announcements,
        "calendar_events": calendar_events,
        "calendar_events_json": calendar_events_json,
    }
    return render(request, "core/dashboard.html", context)
    
    # دروس برای نمایش خلاصه در داشبورد
    if request.user.role == "student":
        subjects = request.user.enrolled_subjects.all()
    elif request.user.role == "teacher":
        subjects = Subject.objects.filter(teacher=request.user)
    else:
        subjects = Subject.objects.all()

    context = {
        "username": request.user.username,
        "role": request.user.role,
        "announcements": announcements,
        "calendar_events": calendar_events,
        "subjects": subjects,
    }
    return render(request, "core/dashboard.html", context)

#calendar
@login_required
def calendar_view(request):
    # تمام رویدادها
    events = CalendarEvent.objects.all().values("id", "title", "description", "date")

    # فرستادن به تمپلیت
    context = {
        "events_json": json.dumps(list(events), default=str),
    }
    return render(request, "core/calendar.html", context)

@login_required
def subjects_view(request):
    if request.user.role == "student":
        subjects = request.user.enrolled_subjects.all()
    elif request.user.role == "teacher":
        subjects = Subject.objects.filter(teacher=request.user)
    else:
        subjects = Subject.objects.all()

    return render(request, "core/subjects.html", {"subjects": subjects})
