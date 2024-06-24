from rest_framework import serializers

from quotation.models import Emirate, Freezone, FreezoneInEmirates, Quotation

class EmirateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emirate
        fields = '__all__'


class FreezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freezone
        fields = ['id', 'name']


class FreezoneInEmiratesSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.freezone.id
    
    def get_name(self, obj):
        return obj.freezone.name
    
    
class BusinessInFreezoneSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.business.id
    
    def get_name(self, obj):
        return obj.business.name


class VisaPackageSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    number_of_package = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.visa_packages.id
    
    def get_number_of_package(self, obj):
        return obj.visa_packages.number_of_package


class QuotationGetSerialzer(serializers.Serializer):
    emirate_id = serializers.IntegerField()
    freezone_id = serializers.IntegerField()
    business_activity_id = serializers.IntegerField()
    visa_package_id = serializers.IntegerField()

    
class QuotationSerialzer(serializers.ModelSerializer):
    emirate = serializers.SerializerMethodField()
    freezone = serializers.SerializerMethodField()
    business_activity = serializers.SerializerMethodField()
    visa_packages = serializers.SerializerMethodField()
    class Meta:
        model = Quotation
        fields = '__all__'

    def get_emirate(self, obj):
        return obj.emirate.name
    
    def get_freezone(self, obj):
        return obj.freezone.name
    
    def get_business_activity(self, obj):
        return obj.business_activity.name
    
    def get_visa_packages(self, obj):
        return obj.visa_packages.number_of_package


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
