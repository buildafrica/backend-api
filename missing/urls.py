from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from .views import (MissingReportCreateView, MissingReportRetrieveUpdateAPIView, MissingReportListAPIView)

urlpatterns = [
    path('reports/$', MissingReportListAPIView.as_view(), name="missing-report-list"),
    path('report/create/$', MissingReportCreateView.as_view(), name="missing-report-create"),
    path('report/<int:id>/$', MissingReportRetrieveUpdateAPIView.as_view(),name="missing-report-update"),
]

