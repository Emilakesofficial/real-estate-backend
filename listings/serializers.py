from rest_framework import serializers
from .models import *
        
class PropertySerializer(serializers.ModelSerializer):
    agent_name = serializers.SerializerMethodField()
    agent_phoneNumber = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = [
            'id',  'agent_name','agent_phoneNumber', 'title', 'property_type', 'description', 'state',
            'country', 'location', 'bathroom', 'bedroom', 'size', 'is_published',
            'price', 'is_active', 'created_at', 'main_image', 'image1', 'image2', 'image3', 'image4',
        ]
        read_only_fields = ['id', 'is_active', 'created_at', 'user', 'agent']

    def get_agent_name(self, obj):
        return f"{obj.agent.first_name} {obj.agent.last_name}"
    def get_agent_phoneNumber(self, obj):
        return obj.agent.profile.phone_number or ""


    def create(self, validated_data):
        request = self.context['request']
        validated_data['agent'] = request.user
        validated_data['user'] = request.user
        return Property.objects.create(**validated_data)

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ['id', 'property', 'message', 'replied_at', 'reply', 'created_at']
        read_only_fields = ['id', 'property', 'user', 'created_at', 'replied_at']
        
    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)


