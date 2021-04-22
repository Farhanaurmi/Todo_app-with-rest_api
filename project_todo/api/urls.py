from django.urls import path
from . import views


urlpatterns = [

    path('allcompletedapi/', views.allcompletedapi.as_view(), name='allcompletedapi'),

]