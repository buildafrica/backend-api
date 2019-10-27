from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import MissingReportSerializer
from .models import MissingReport

class MissingReportCreateView(CreateAPIView):
    serializer_class = MissingReportSerializer
    permission_classes = (IsAuthenticated,)
    parser_class = (FileUploadParser,)
    allowed_methods = ("POST",)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):

        serializer = MissingReportSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(reported_by=self.request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MissingReportRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = MissingReportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    allowed_methods = ("GET", "PATCH")

    def get_queryset(self):
        return MissingReport.objects.filter(reported_by=self.request.user)
        

class MissingReportListAPIView(ListAPIView):    
    serializer_class = MissingReportSerializer
    permission_classes = (AllowAny,)
    allowed_methods = ("GET",)

    def get_queryset(self):
        return MissingReport.objects.filter(isActive=True)