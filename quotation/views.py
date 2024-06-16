from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from quotation.api.v1.services.create_pdf import CreatePdf
from quotation.models import BusinessInFreezone, Emirate, FreezoneInEmirates, Quotation, VisaPackagesInBusiness
from quotation.serializers import BusinessInFreezoneSerializer, EmirateSerializer, FreezoneInEmiratesSerializer, QuotationSerialzer, VisaPackageSerializer
# Create your views here.

class QuotationView(APIView):

    def get(self, request, *args, **kwargs):
        emirate_id = request.query_params.get('emirate_id')
        freezone_id = request.query_params.get('freezone_id')
        business_activity_id = request.query_params.get('business_activity_id')
        visa_package_id = request.query_params.get('visa_package_id')

        quotation = Quotation.objects.filter(emirate_id=emirate_id, 
                                             freezone_id=freezone_id, 
                                             business_activity_id=business_activity_id, 
                                             visa_packages=visa_package_id).last()
        
        quotation_data = QuotationSerialzer(quotation).data
        pdf_file = CreatePdf().generate_pdf(quotation_data)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="business_license_report.pdf"'
        return response
    

class EmiratesView(APIView):

    def get(self, request, *args, **kwargs):
        emirates = Emirate.objects.all()
        serializer = EmirateSerializer(emirates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK, headers={
            'ngrok-skip-browser-warning': '1231'
        })
    

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
        freezone_and_emirate = FreezoneInEmirates.objects.filter(emirate_id=emirate_id, freezone_id=freezone_id).last()
        business = BusinessInFreezone.objects.filter(freezone_and_emirate=freezone_and_emirate)
        serializer = BusinessInFreezoneSerializer(business, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PackageView(APIView):

    def get(self, request, *args, **kwargs):
        emirate_id = self.kwargs['emirate_id']
        freezone_id = self.kwargs['freezone_id']
        business_id = self.kwargs['business_id']
        freezone_and_emirate = FreezoneInEmirates.objects.filter(emirate_id=emirate_id, freezone_id=freezone_id)
        business = BusinessInFreezone.objects.filter(freezone_and_emirate__in=freezone_and_emirate, business=business_id)
        visa_package_in_business = VisaPackagesInBusiness.objects.filter(business_in_freezone__in=business)
        serializer = VisaPackageSerializer(visa_package_in_business, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)