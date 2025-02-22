from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50, unique=True)
    face_encoding = models.BinaryField()  # Store face encodings as binary
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return self.name
