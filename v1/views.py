from rest_framework import generics

from .models import Case, Sighting, User
from .serializers import CaseSerializer, SightingSerializer
from .permissions import IsOwnerOrReadOnly

class CaseView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class CaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating or deleting an Event instance.
    '''
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class SightingView(generics.ListCreateAPIView):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer


class CaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating or deleting an Event instance.
    '''
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (IsOwnerOrReadOnly,)