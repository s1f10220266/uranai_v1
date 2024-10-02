from django.urls import path
from . import views

urlpatterns = [
    path('', views.title, name='title'),
    path('main', views.index, name='index'),
    path('output/<int:scenario_id>', views.result, name='output'),
]
