from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Itinerary, Destination
from markdown import markdown


# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
        else:
            
            return HttpResponse("Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def dashboard_view(request):
    if request.user.is_authenticated:
        # Fetch user-specific data if needed
        user_itineraries = Itinerary.objects.filter(user=request.user).order_by('-created_at')
    
    # Suggested itineraries (Fetching random itineraries)
        suggested_destinations = Destination.objects.all()[:5]
        return render(request, 'dashboard.html', {
            'user_itineraries': user_itineraries,
            'suggested_destinations': suggested_destinations
            })

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout
def generate_views(request):
    return render(request, 'generate_form.html')

from .services import get_weather

def display_itinerary(request):
    city_name = request.GET.get('destination')

    weather_data = get_weather(city_name)  # 👈 ADD THIS for debugging
    print("🔍 Context being passed to template:", {
    'weather_data': weather_data,
    'destination': city_name,
    })
    context = {
    'weather_data': weather_data,
    'city': city_name,
    'source': request.GET.get('source'),
    'destination': city_name,
    'start_date': request.GET.get('start_date'),
    'end_date': request.GET.get('end_date'),
    'budget': request.GET.get('budget'),
    'itinerary': request.GET.get('itinerary', 'No itinerary available')
    }
    print("🧪 Context sent to template:", context)
    return render(request, 'display.html', context)

 


from .reg_form import RegisterForm
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('dashboard')  # Redirect to a dashboard or home page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
    
from django.http import JsonResponse
from .services import generate
from .models import Itinerary
import json
from bs4 import BeautifulSoup

@login_required
def itinerary_generator(request):
    if request.method == 'GET':
        # Extract query parameters
        source = request.GET.get('source')
        destination = request.GET.get('destination')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        no_of_days = request.GET.get('no_of_days')
        travel_mode = request.GET.get('travel_mode')
        budget = request.GET.get('budget',"0")
        # Call the service to generate itinerary
        itinerary = generate(source, destination, start_date, end_date, no_of_days,travel_mode, budget)
        print("GET Params:", request.GET)
        print(f"Source: {source}, Destination: {destination}, Start: {start_date}, End: {end_date}, No of Days: {no_of_days},Travel:{travel_mode}, Budget: {budget}")
        weather_data = get_weather(destination, start_date, end_date)
        weather_data = weather_data[:int(no_of_days)]
        print("🌤️ Weather Data:", weather_data)

        itinerary = markdown(itinerary)
        soup = BeautifulSoup(itinerary, "html.parser")
        
        itinerary = soup.get_text()
        if not itinerary:
            return JsonResponse({"error": "Failed to generate itinerary"}, status=500)

       
        
        # Save the itinerary to the database
        Itinerary.objects.create(
            user=request.user,
            title=f"Trip from {source} to {destination}",
            start_date=start_date,
            end_date=end_date,
            budget=budget,  # Optional: Adjust if budget is available
            destinations=json.dumps([source, destination]),
            content=itinerary,
        )

        return render(request, 'display.html', {
        'source': source,
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date,
        'no_of_days': no_of_days,
        'travel_mode': travel_mode,
        'budget': budget,
        'itinerary': itinerary,
        'weather_data': weather_data
        })

def save_itinerary(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        source = data.get('source')
        destination = data.get('destination')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        travel_mode = data.get('travel_mode')
        budget= data.get('budget')
        itinerary = data.get('itinerary')

        # Save to the database
        Itinerary.objects.create(
            user=request.user,
            title=f"Trip from {source} to {destination}",
            start_date=start_date,
            end_date=end_date,
            travel_mode=travel_mode,
            budget=budget,  # Optional
            destinations=json.dumps([source, destination]),
            content=itinerary
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Itinerary

def delete_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    itinerary.delete()
    return redirect('dashboard')  # Redirect to the page showing all itineraries



def itinerary_detail(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    return render(request, 'itinerary_detail.html', {'itinerary': itinerary})

from django.http import HttpResponse
from django.urls import reverse
def download_pdf(request):
    pdf_url = reverse('download_pdf') 
    # Temporary response - Replace with actual PDF logic
    return HttpResponse("PDF download feature coming soon!", content_type="text/plain")


from .models import Expense, Itinerary
from .expense_forms import ExpenseForm


from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth

def track_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('track_expenses')  # Stay on the same page after form submission
    else:
        form = ExpenseForm()

    expenses = Expense.objects.all()  # Retrieve all expenses

    # **Fixed: Use actual_cost instead of amount**
    total_expense = expenses.aggregate(Sum('actual_cost'))['actual_cost__sum'] or 0.0
    
    # Convert total_expense to Decimal if it's a float
    total_expense = Decimal(total_expense)

    category_expenses = expenses.values('category').annotate(total=Sum('actual_cost')).order_by('-total')

    monthly_expenses = expenses.annotate(month=TruncMonth('created_at')) \
        .values('month').annotate(total=Sum('actual_cost')).order_by('month')

    budgeted_amount = Itinerary.objects.aggregate(Sum('budget'))['budget__sum'] or Decimal('0.00')

    over_budget = total_expense > budgeted_amount
    remaining_budget = max(budgeted_amount - total_expense, Decimal('0.00'))
    exceeded_by = max(total_expense - budgeted_amount, Decimal('0.00'))

    top_categories = category_expenses[:5]

    context = {
        'form': form,
        'expenses': expenses,
        'total_expense': total_expense,
        'category_expenses': category_expenses,
        'monthly_expenses': monthly_expenses,
        'budgeted_amount': budgeted_amount,
        'over_budget': over_budget,
        'remaining_budget': remaining_budget,
        'exceeded_by': exceeded_by,
        'top_categories': top_categories,
    }

    return render(request, 'track_expenses.html', context)

import os
PLACES_API_KEY = os.getenv('PLACES_API_KEY')

from .services import get_places
from .utils import get_coordinates  # Optional utility to get lat/lng from city
from django.conf import settings
def get_top_places(results, top_n=5,min_reviews=5):
    # Filter out places without rating and sort by rating (descending)
    sorted_places = sorted(
        [place for place in results if 'rating' in place and place.get('user_ratings_total', 0) >= min_reviews],
        key=lambda x: x['rating'],
        reverse=True
    )
    return sorted_places[:top_n]
def places(request):
    city_name = request.GET.get('destination')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    print(f"Destination: {city_name}, Start: {start_date}, End: {end_date}")

    if city_name and start_date and end_date:
        lat, lng = get_coordinates(city_name, settings.PLACES_API_KEY)
        print(f"Coordinates for {city_name}: {lat}, {lng}")

        all_restaurants = get_places(lat, lng, 'restaurant', settings.PLACES_API_KEY)
        all_hotels = get_places(lat, lng, 'lodging', settings.PLACES_API_KEY)
        attractions = get_places(lat, lng, 'tourist_attraction', settings.PLACES_API_KEY)
        restaurants = get_top_places(all_restaurants)
        hotels = get_top_places(all_hotels)
    else:
        lat = lng = None
        restaurants = hotels = attractions=[]
        print("No valid coordinates found.")

    context = {
        'city': city_name,
        'weather_data': get_weather(city_name, start_date, end_date) if city_name else [],
        'hotels': hotels,
        'restaurants': restaurants,
        'attractions': attractions,
    }

    return render(request, 'places.html', context)
