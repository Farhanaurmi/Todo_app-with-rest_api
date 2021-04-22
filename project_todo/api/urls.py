from django.urls import path
from . import views


urlpatterns = [
    path('allcompleteapi', views.allcompletedapi.as_view()),
    path('todos', views.todosapi.as_view()),
    path('todos/<int:pk>', views.viewtodosapi.as_view()),
    path('todos/<int:pk>/complete', views.completeapi.as_view()),

]