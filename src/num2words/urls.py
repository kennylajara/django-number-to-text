from django.urls import path

from . import views

urlpatterns = [
    path("num_to_english", views.number_to_english, name="num_to_english"),
]
