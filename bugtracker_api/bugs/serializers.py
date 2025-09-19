from rest_framework import serializers
from .models import Bug
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class BugSerializer(serializers.ModelSerializer):
    reported_by = UserSerializer(read_only=True)

    class Meta:
        model = Bug
        fields = '__all__'
        read_only_fields = ("title","description","status","priority","screenshot","assigned_to","reported_by", "created_at", "updated_at")
