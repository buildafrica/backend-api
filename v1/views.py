from rest_framework import generics

from .models import Case, UserProfile, Sighting
from .serializers import CaseSerializer, UserProfileSerializer, SightingSerializer

class CaseView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class SightingView(generics.ListCreateAPIView):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer
