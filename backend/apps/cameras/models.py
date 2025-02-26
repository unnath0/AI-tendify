from django.db import models


class Camera(models.Model):
    camera_id = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    source_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Camera {self.camera_id} - {self.location}"


class EngagementRecord(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    face_count = models.IntegerField()
    engaged_count = models.IntegerField()

    @property
    def engagement_percentage(self):
        if self.face_count == 0:
            return 0
        return round((self.engaged_count / self.face_count) * 100, 2)

    def __str__(self):
        return f"{self.camera.camera_id} - {self.timestamp} - {self.engagement_percentage}% Engaged"
