from rest_framework import generics,permissions
from .serializers import *
from app_todo.models import TodoClass



class allcompletedapi(generics.ListAPIView):
    serializer_class=TodoClassSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        todos=TodoClass.objects.filter(user=user,dtime__isnull=False).order_by('-dtime')
        return todos


