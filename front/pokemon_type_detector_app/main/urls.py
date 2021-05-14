from django.urls import path
from .views import main_func 
urlpatterns = [
    path('', main_func, name="main"),
]
