from django.urls import path
from endpoint import views

urlpatterns = [
    path('opening-hours/', views.Schedule_endpoint),

]
