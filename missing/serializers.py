from rest_framework import serializers
from .models import MissingReport


class MissingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingReport
        exclude = ("date_modified", "date_created", "isActive")
     
