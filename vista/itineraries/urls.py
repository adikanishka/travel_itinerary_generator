from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include
from .views import download_pdf,delete_itinerary

urlpatterns = [
    path('', views.index, name='home'),
    path('generate-itinerary/', views.itinerary_generator, name='generate_itinerary'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('generate/', views.generate_views, name='generate'),
    path('admin/', admin.site.urls , name='admin'),
    path('display/',views.display_itinerary,name='display'),
    path('save-itinerary/', views.save_itinerary, name='save_itinerary'),
    path('itinerary/<int:itinerary_id>/', views.itinerary_detail, name='itinerary_detail'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('track-expenses/', views.track_expenses, name='track_expenses'),
     path('delete/<int:itinerary_id>/', delete_itinerary, name='delete_itinerary' ),
]