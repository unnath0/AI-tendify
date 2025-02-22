# import cv2
import numpy as np
import face_recognition
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Student
from .serializers import StudentSerializer
from django.conf import settings
import os


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Student(s) added successfully",
                    "processed_students": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


# View to Retrieve, Update, or Delete a Student by student_id
class StudentRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "student_id"  # Fetch students by their ID instead of default 'pk'

    def patch(self, request, *args, **kwargs):
        student = self.get_object()
        student.is_present = request.data.get("is_present", student.is_present)
        student.save()
        return Response({"message": f"Student {student.student_id} attendance updated"})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Student {instance.student_id} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class FaceEncodingAPIView(APIView):
    def post(self, request):
        if "images" not in request.FILES:
            return Response(
                {"error": "At least one image is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        images = request.FILES.getlist("images")  # Handle multiple files
        processed_students = []
        errors = []
        file_paths = []

        for image_file in images:
            file_name = os.path.splitext(image_file.name)[
                0
            ]  # Extract filename without extension
            student_id = file_name  # Assuming filename is the student ID

            try:
                # Check if student exists in database
                student = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                errors.append({"student_id": student_id, "error": "Student not found"})
                continue

            # Save the file
            file_path = default_storage.save(f"media/{image_file.name}", image_file)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            file_paths.append(full_path)

            # Process image
            image = face_recognition.load_image_file(full_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if len(face_encodings) != 1:
                errors.append(
                    {
                        "student_id": student_id,
                        "error": "Image must contain exactly one face",
                    }
                )
                continue

            # Store face encoding
            encoding = face_encodings[0].tobytes()
            student.face_encoding = encoding
            student.save()

            processed_students.append({"student_id": student_id, "name": student.name})

            # cleanup, removing the images in media
            for path in file_paths:
                if os.path.exists(path):
                    os.remove(path)

        return Response(
            {
                "message": "Face encodings processed",
                "processed_students": processed_students,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )


class FaceRecognitionAPIView(APIView):
    def post(self, request):
        if "images" not in request.FILES:
            return Response(
                {"error": "At least one image is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        images = request.FILES.getlist("images")  # Get multiple images
        students_marked = set()  # Use a set to avoid duplicates
        file_paths = []

        # Load all student encodings into a NumPy array at once
        students = Student.objects.exclude(face_encoding__isnull=True).exclude(
            face_encoding=b""
        )
        student_ids = []
        known_encodings = []

        for student in students:
            encoding = np.frombuffer(student.face_encoding)
            if encoding.shape[0] == 128:  # Ensure valid encoding
                known_encodings.append(encoding)
                student_ids.append(student.student_id)

        if not known_encodings:
            return Response(
                {"error": "No valid encodings found in the database"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        known_encodings = np.array(known_encodings)  # Convert to NumPy matrix

        for image_file in images:
            file_path = default_storage.save(f"media/{image_file.name}", image_file)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            file_paths.append(full_path)

            # Process the image
            image = face_recognition.load_image_file(full_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            for encoding in face_encodings:
                # Compute distances using NumPy broadcasting
                distances = np.linalg.norm(known_encodings - encoding, axis=1)
                best_match_index = np.argmin(distances)  # Find closest match

                if distances[best_match_index] < 0.5:  # Stricter threshold
                    student_id = student_ids[best_match_index]
                    if student_id not in students_marked:  # Avoid duplicates
                        student = Student.objects.get(student_id=student_id)
                        student.is_present = True
                        student.save()
                        students_marked.add(student_id)

        # Cleanup: Remove uploaded images
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)

        # Convert set to list of dictionaries
        marked_students_list = [
            {
                "student_id": student_id,
                "name": Student.objects.get(student_id=student_id).name,
            }
            for student_id in students_marked
        ]

        return Response(
            {"marked_present": marked_students_list}, status=status.HTTP_200_OK
        )


class StudentListAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
