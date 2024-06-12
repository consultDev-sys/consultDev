from rest_framework import serializers

from quotation.models import Emirate, Freezone, FreezoneInEmirates

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

