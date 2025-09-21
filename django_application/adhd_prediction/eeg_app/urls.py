from django.urls import path
from . import views

urlpatterns = [
    path('', views.eeg_input, name='eeg_input'),
    path('predict/', views.predict_adhd, name='predict_adhd'),
]