from django.urls import path
from .views import (
    FaceRecognitionAPIView,
    StudentListAPIView,
    FaceEncodingAPIView,
    StudentListCreateAPIView,
    StudentRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path("recognize/", FaceRecognitionAPIView.as_view(), name="face-recognition"),
    path("retrieve_all/", StudentListAPIView.as_view(), name="students-list"),
    path("encode/", FaceEncodingAPIView.as_view(), name="face-encoding"),
    path("add/", StudentListCreateAPIView.as_view(), name="add-student"),
    path(
        "update/<str:student_id>/",
        StudentRetrieveUpdateDeleteAPIView.as_view(),
        name="update-student",
    ),
]
