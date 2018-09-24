from rest_framework import generics, permissions

from .models import Case, Sighting
from .serializers import CaseSerializer, SightingSerializer
from .permissions import IsOwnerOrReadOnly

class CaseView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class CaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating or deleting a Case instance.
    '''
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class SightingView(generics.ListCreateAPIView):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class SightingDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating or deleting a Sighting instance.
    '''
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)