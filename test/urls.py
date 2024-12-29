from django.urls import path
from test import views

urlpatterns = [
    path('test/', views.test, name='test'),

]