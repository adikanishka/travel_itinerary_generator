from django.contrib import admin

# Register your models here.
from .models import Destination, SuggestedItinerary

admin.site.register(Destination)

admin.site.register(SuggestedItinerary)


class SuggestedItineraryAdmin(admin.ModelAdmin):
    filter_horizontal = ('destinations',)

from .models import Feedback

admin.site.register(Feedback)