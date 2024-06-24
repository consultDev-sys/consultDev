from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

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
        serializer = QuotationGetSerialzer(data=query_params)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        query_params = serializer.validated_data
        quotation = Quotation.objects.filter(emirate_id=query_params["emirate_id"], 
                                             freezone_id=query_params["freezone_id"], 
                                             business_activity_id=query_params["business_activity_id"], 
                                             visa_packages=query_params["visa_package_id"]).last()
        
        quotation_data = QuotationSerialzer(quotation).data
        pdf_file = CreatePdf().generate_pdf(quotation_data)
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
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            customer_id = request.user.id
            
            s3_service = S3Service()
            image_url = s3_service.upload_image(image, customer_id)
            
            if image_url:
                return Response({'image_url': image_url}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to upload image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)