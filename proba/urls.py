from django.urls import path
from proba import views

urlpatterns = [
    path('lois/', views.lois, name='lois'),

]