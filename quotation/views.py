from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

from consultancy.base_service import BaseService
from customer_auth.helpers import get_error_string_from_serializer_error_object
from quotation.api.v1.services.bucket_service import S3Service
from quotation.api.v1.services.create_pdf import CreatePdf
from quotation.models import BusinessInFreezone, Emirate, FreezoneInEmirates, Quotation, VisaPackagesInBusiness
from quotation.serializers import (BusinessInFreezoneSerializer, 
                                   EmirateSerializer, 
                                   FreezoneInEmiratesSerializer, ImageUploadSerializer, 
                                   QuotationGetSerialzer, 
                                   QuotationSerialzer, 
                                   VisaPackageSerializer
                                   )
# Create your views here.

class QuotationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        customer = request.user
        serializer = QuotationGetSerialzer(data=query_params)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        query_params = serializer.validated_data
        quotation = Quotation.objects.filter(emirate_id=query_params["emirate_id"], 
                                             freezone_id=query_params["freezone_id"], 
                                             business_activity_id=query_params["business_activity_id"], 
                                             visa_packages=query_params["visa_package_id"]).last()
        
        quotation_data = QuotationSerialzer(quotation).data
        logo = query_params.get('logo', None)
        pdf_file = CreatePdf().generate_pdf(customer, quotation_data, logo)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="business_license_report.pdf"'
        return response
    

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
    

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.FILES)
        if not serializer.is_valid():
            response = BaseService.send_response(errors=get_error_string_from_serializer_error_object(serializer.errors), 
                                                code=status.HTTP_400_BAD_REQUEST,
                                                message="Validation error")
            return Response(response, status=response["code"])
            
        image = serializer.validated_data['image']
        customer_id = request.user.id
        s3_service = S3Service()
        response = s3_service.upload_image(image, customer_id)
        return Response(response, status=response["code"])
