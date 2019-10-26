from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

from Util.models import BaseModel

class MissingReport(BaseModel):
    help_text = "Stores the data related a reported missing person"
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    missing_since = models.DateField()
    last_seen = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    image_upload = models.ImageField(upload_to="mpa/images", null=True, blank=True)
    image_upload_thumbnail = ImageSpecField(
        source="image_upload",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 60},
    )    
    
    
    def __str__(self):
        return self.name
