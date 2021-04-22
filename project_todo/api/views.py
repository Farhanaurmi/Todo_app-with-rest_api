from rest_framework import generics,permissions
from .serializers import *
from app_todo.models import TodoClass
from django.utils import timezone



class allcompletedapi(generics.ListAPIView):
    serializer_class=TodoClassSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        todos=TodoClass.objects.filter(user=user,dtime__isnull=False).order_by('-dtime')
        return todos

class todosapi(generics.ListCreateAPIView):
    serializer_class=TodoClassSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user=self.request.user
        todos=TodoClass.objects.filter(user=user, dtime__isnull=True)
        return todos

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class viewtodosapi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TodoClassSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user=self.request.user
        todos=TodoClass.objects.filter(user=user)
        return todos


class completeapi(generics.UpdateAPIView):
    serializer_class=CompleteSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        todos=TodoClass.objects.filter(user=user)
        return todos


    def perform_update(self,serializer):
        serializer.instance.dtime=timezone.now()
        serializer.save()





