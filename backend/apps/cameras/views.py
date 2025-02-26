from django.http import StreamingHttpResponse
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import cv2
import threading
import numpy as np
from .models import Camera, EngagementRecord
from .serializers import CameraSerializer, EngagementRecordSerializer
# from utils.ai_model import analyze_frame

camera_streams = {}


class CameraStream:
    def __init__(self, camera_id, source=0):
        self.camera_id = camera_id
        self.source = (
            int(source) if source.isdigit() else source
        )  # Ensure correct format
        self.capture = cv2.VideoCapture(self.source)
        self.lock = threading.Lock()

        if not self.capture.isOpened():
            print(f"❌ ERROR: Camera {self.camera_id} failed to open!")

    def get_frame(self):
        with self.lock:
            ret, frame = self.capture.read()
            if not ret:
                print(f"⚠️ WARNING: Failed to read frame from Camera {self.camera_id}")
                return None
            return frame


def generate_frames(camera_id):
    print(f"🎥 Streaming frames for camera {camera_id}...")

    while True:
        frame = camera_streams[camera_id].get_frame()
        if frame is None:
            print(f"⚠️ WARNING: No frame from {camera_id}, skipping...")
            continue  # Skip if frame capture failed

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


class CameraListAPIView(generics.ListCreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class LiveFeedAPIView(APIView):
    def get(self, request, camera_id):
        if camera_id not in camera_streams:
            try:
                camera = Camera.objects.get(camera_id=camera_id)
                source = (
                    camera.source_url if camera.source_url else 0
                )  # Use system camera if no URL
                camera_streams[camera_id] = CameraStream(camera_id, source)
            except Camera.DoesNotExist:
                return Response(
                    {"error": "Camera not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return StreamingHttpResponse(
            generate_frames(camera_id),
            content_type="multipart/x-mixed-replace; boundary=frame",
        )


# class EngagementAnalysisAPIView(APIView):
#     def post(self, request, camera_id):
#         if "frame" not in request.FILES:
#             return Response(
#                 {"error": "No frame provided"}, status=status.HTTP_400_BAD_REQUEST
#             )
#
#         frame = request.FILES["frame"].read()
#         nparr = np.frombuffer(frame, np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#         result = analyze_frame(img)  # AI model function
#
#         face_count = len(result["engagement_analysis"])
#         engaged_count = sum(
#             1 for face in result["engagement_analysis"] if face["engaged"]
#         )
#
#         camera = Camera.objects.get(camera_id=camera_id)
#         record = EngagementRecord.objects.create(
#             camera=camera, face_count=face_count, engaged_count=engaged_count
#         )
#
#         return Response(
#             {
#                 "engagement_percentage": record.engagement_percentage,
#                 "faces_detected": face_count,
#                 "engaged_faces": engaged_count,
#                 "detailed_analysis": result["engagement_analysis"],
#             },
#             status=status.HTTP_200_OK,
#         )
#


class EngagementHistoryAPIView(generics.ListAPIView):
    serializer_class = EngagementRecordSerializer

    def get_queryset(self):
        camera_id = self.kwargs.get("camera_id")
        return EngagementRecord.objects.filter(camera__camera_id=camera_id).order_by(
            "-timestamp"
        )
