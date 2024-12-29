from django.urls import path
from pandass import views

urlpatterns = [
    path('', views.index, name='show'),

    path('upload/', views.upload, name='upload'),
    path('list_files/', views.list_uploaded_files, name='list_files'),
    path('uploadlink/', views.uploadLink, name='uploadlink'),
    path('download/', views.download, name='download'),
    

]

