from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Trip
import random


# -------- AI GENERATOR --------
def generate_plan(destination, days, budget, interests):
    itinerary = []
    interests_list = interests.lower().split(',')

    activities = {
        "beach": ["Beach Visit", "Sunset View", "Water Sports"],
        "food": ["Street Food Tour", "Restaurant Visit"],
        "adventure": ["Trekking", "Boating", "Parasailing"],
        "history": ["Museum", "Fort Visit"]
    }

    selected = []

    for i in interests_list:
        i = i.strip()
        if i in activities:
            selected.extend(activities[i])

    if not selected:
        selected = ["City Tour", "Relaxation", "Shopping"]

    cost_per_day = int(budget) // int(days)

    weather = random.choice(["Sunny ☀️", "Cloudy ☁️", "Pleasant 🌤️"])
    hotel = random.choice(["Budget Inn", "Comfort Stay", "Luxury Palace"])

    recommendation = f"Based on your interests, {destination} is a great choice for a balanced trip."

    for d in range(1, int(days)+1):
        act = random.choice(selected)

        plan = f"""
Day {d} - {destination}

Weather: {weather}

Morning: {act}
Afternoon: Explore local area
Evening: Food & Relax

Suggested Stay: {hotel}
Estimated Cost: ₹{cost_per_day}
"""
        itinerary.append(plan)

    itinerary.insert(0, f"✨ Smart Recommendation:\n{recommendation}\n")

    return itinerary


# -------- HOME --------
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    itinerary = None
    analysis = None

    if request.method == 'POST':
        destination = request.POST['destination']
        days = request.POST['days']
        budget = request.POST['budget']
        interests = request.POST['interests']

        plan_list = generate_plan(destination, days, budget, interests)
        plan_text = "\n".join(plan_list)

        Trip.objects.create(
            user=request.user,
            destination=destination,
            days=days,
            budget=budget,
            interests=interests,
            itinerary=plan_text
        )

        itinerary = plan_list

        analysis = {
            "transport": int(int(budget) * 0.3),
            "food": int(int(budget) * 0.3),
            "stay": int(int(budget) * 0.4)
        }

    trips = Trip.objects.filter(user=request.user).order_by('-id')
    total_trips = trips.count()

    return render(request, 'home.html', {
        'itinerary': itinerary,
        'trips': trips,
        'analysis': analysis,
        'total_trips': total_trips
    })


# -------- DOWNLOAD --------
def download_plan(request, trip_id):
    trip = Trip.objects.get(id=trip_id, user=request.user)

    response = HttpResponse(trip.itinerary, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{trip.destination}_plan.txt"'

    return response


# -------- SIGNUP --------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)

        return redirect('/login/')

    return render(request, 'signup.html')


# -------- LOGIN --------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Wrong credentials'})

    return render(request, 'login.html')


# -------- LOGOUT --------
def logout_view(request):
    logout(request)
    return redirect('/login/')