from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from .models import Bug
from rest_framework.decorators import api_view,  parser_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import BugSerializer
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def bug_list(request):
    if request.method == 'GET':
        bugs = Bug.objects.all().order_by('-created_at')
        serializer = BugSerializer(bugs, many=True)
        return Response(serializer.data)

class BugViewSet(viewsets.ModelViewSet):
    queryset = Bug.objects.all().order_by('-created_at')
    serializer_class = BugSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        guest_user = User.objects.get_or_create(username="guest")[0]
        serializer.save(reported_by=guest_user)

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id','username','password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User(username=validated_data['username'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
    

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer

