from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from .models import Bug
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BugSerializer

@api_view(['GET'])
def bug_list(request):
    bugs = Bug.objects.all().order_by('-created_at')
    serializer = BugSerializer(bugs, many=True)
    return Response(serializer.data)

# class BugListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Bug.objects.all().order_by('-created_at')
#     serializer_class = BugSerializer
#     permission_classes = [permissions.IsAuthenticated]                      

#     def get_queryset(self):
#         # show all bugs OR only user’s bugs (your choice)
#         return Bug.objects.all().order_by('-created_at')
    

# class BugRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Bug.objects.all()
#     serializer_class = BugSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # user can only edit/delete their own bugs
#         return Bug.objects.filter(reported_by=self.request.user)

class BugViewSet(viewsets.ModelViewSet):
    queryset = Bug.objects.all().order_by('-created_at')
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

