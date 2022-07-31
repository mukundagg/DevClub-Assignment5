from Users import models as user_models
from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from . import serializers as api_serializers
# Create your views here.

class MemberViewSet(viewsets.ModelViewSet):
    """
        API endpoint allowing members to be viewed or edited
    """
    queryset = user_models.Member.objects.all().order_by("dateJoined");
    serializer_class = api_serializers.MemberSerializer;
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    """
        API endpoint allowing members to be viewed or edited
    """
    queryset = user_models.Course.objects.all();
    serializer_class = api_serializers.CourseSerializer;
    permission_classes = [permissions.IsAuthenticated]