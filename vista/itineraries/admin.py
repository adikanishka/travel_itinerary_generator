from django.contrib import admin

# Register your models here.
from .models import Destination, Itinerary

admin.site.register(Destination)

admin.site.register(Itinerary)

