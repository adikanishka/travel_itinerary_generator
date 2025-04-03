from django.db import models
from django.contrib.auth.models import User
import json

# Store AI-Generated Itineraries
class Itinerary(models.Model):
    TRAVEL_MODE_CHOICES = [
        ("car", "Car"),
        ("bus", "Bus"),
        ("train", "Train"),
        ("flight", "Flight"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    travel_mode = models.CharField(
        max_length=10,
        choices=TRAVEL_MODE_CHOICES,
        default="car"
    )
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    destinations = models.TextField()  # Simplified: store as JSON string
    content = models.TextField()       #  AI-generated itinerary text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username} {self.budget})"
    
    # Method to convert destinations field to a Python list
    def get_destinations(self):
        return json.loads(self.destinations) if self.destinations else []

#  Optional: Store Popular Destinations for Recommendations
class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('transport', 'Transport'),
        ('accommodation', 'Accommodation'),
        ('food', 'Food'),
        ('activities', 'Activities'),
        ('miscellaneous', 'Miscellaneous'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.category} - {self.estimated_cost}"
    



