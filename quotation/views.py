from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

class QuotationView(APIView):

    def post(self, request, *args, **kwargs):
        print(request)
        return Response(data="My first api", status=200)