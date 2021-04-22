from rest_framework import generics,permissions
from .serializers import *
from app_todo.models import TodoClass
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


@csrf_exempt
def signup(request):
    if request.method=='POST':
        try:
            data=JSONParser().parse(request)
            user=User.objects.create_user(data['username'],password=data['password'])
            user.save()
            token=Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=200)

        except IntegrityError:
            return JsonResponse({'error':'user name has been taken'},status=400)


@csrf_exempt
def login(request):
    if request.method=='POST':
        data=JSONParser().parse(request)
        user=authenticate(data['username'],password=data['password'])
        if user is None:
            return JsonResponse({'error':'try again'},status=400)
            
        else:
            try:
                token=Token.objects.get(user=user)
            except:
                token=Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=200)

       


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


      



