from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Election_Area, Details, Main
from . serializers import easerializers, detailserializer, mainserializer
from rest_framework.viewsets import ViewSet
from rest_framework import permissions

class ElectionAreaViewSet(ViewSet):
    
    def list(self,request):
        area = Election_Area.objects.all()
        serializer = easerializers(area,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    
class DetailsViewSet(ViewSet):
    queryset = Details.objects.all()
    serializer_class = detailserializer
    
class MainViewSet(ViewSet):
    
    def list(self,request):
        data = Main.objects.all()
        serializer = mainserializer(data,many=True)
        return Response(serializer.data)
        