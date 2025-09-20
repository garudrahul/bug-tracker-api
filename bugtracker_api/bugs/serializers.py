from rest_framework import serializers
from .models import Bug
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class BugSerializer(serializers.ModelSerializer):
    screenshot = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Bug
        fields = '__all__'
        read_only_fields = ['reported_by', 'created_at'] 
        
    def create(self, validated_data):
        validated_data['reported_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['reported_by'] = self.context['request'].user
        return super().update(instance, validated_data)
