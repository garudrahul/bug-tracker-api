from rest_framework import serializers
from .models import Bug
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class BugSerializer(serializers.ModelSerializer):
    screenshot = serializers.ImageField(use_url=True)
    reported_by = serializers.StringRelatedField(read_only=True)
    
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
