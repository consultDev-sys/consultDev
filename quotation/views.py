from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quotation.models import BusinessInFreezone, Emirate, FreezoneInEmirates
from quotation.serializers import BusinessInFreezoneSerializer, EmirateSerializer, FreezoneInEmiratesSerializer
# Create your views here.

class QuotationView(APIView):

    def get(self, request, *args, **kwargs):

        return Response(data="My first api", status=200)
    

class EmiratesView(APIView):

    def get(self, request, *args, **kwargs):
        emirates = Emirate.objects.all()
        serializer = EmirateSerializer(emirates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class FreezoneView(APIView):

    def get(self, request, *args, **kwargs):
        emirate_id = self.kwargs['emirate_id']
        freezones = FreezoneInEmirates.objects.filter(emirate_id=emirate_id)
        serializer = FreezoneInEmiratesSerializer(freezones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BusinessView(APIView):

    def get(self, request, *args, **kwargs):
        emirate_id = self.kwargs['emirate_id']
        freezone_id = self.kwargs['freezone_id']
        business = BusinessInFreezone.objects.filter(emirate_id=emirate_id, freezone_id=freezone_id)
        serializer = BusinessInFreezoneSerializer(business, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    