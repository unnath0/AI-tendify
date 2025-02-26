from django.urls import path
from .views import (
    CameraListAPIView,
    LiveFeedAPIView,
    # EngagementAnalysisAPIView,
    EngagementHistoryAPIView,
)

urlpatterns = [
    path("", CameraListAPIView.as_view(), name="camera-list"),
    path("<str:camera_id>/", LiveFeedAPIView.as_view(), name="live-feed"),
    # path(
    #     "<str:camera_id>/analyze/",
    #     EngagementAnalysisAPIView.as_view(),
    #     name="engagement-analysis",
    # ),
    path(
        "<str:camera_id>/history/",
        EngagementHistoryAPIView.as_view(),
        name="engagement-history",
    ),
]
