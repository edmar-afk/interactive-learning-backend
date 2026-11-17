
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Lessons, Quiz, QuizQuestion, LessonsVideo, QuizScore, FileUpload

from .serializers import (
    RegisterSerializer,
    StudentsQuizScoreSerializer,
    UserSerializer,
    LessonsSerializer,
    QuizSerializer,
    QuizQuestionSerializer,
    LessonsVideoSerializer, QuizScoreSerializer, FileUploadSerializer
)


# ==========================================================
# REGISTER
# POST /api/register/
# ==========================================================

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "message": "Registration successful!",
                "userInfo": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================================
# LOGIN
# POST /api/login/
# ==========================================================

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({
                "message": "Username and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return Response({
                "message": "Invalid username or password."
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "message": "Login successful!",
            "userInfo": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


# ==========================================================
# LESSONS
# GET  /api/lessons/
# POST /api/lessons/
# ==========================================================

class LessonsListCreateView(generics.ListCreateAPIView):
    queryset = Lessons.objects.select_related(
        "created_by"
    ).prefetch_related(
        "videos",
        "quiz__questions"
    ).order_by("-created_at")

    serializer_class = LessonsSerializer
    permission_classes = [AllowAny]


# ==========================================================
# LESSON DETAIL
# GET    /api/lessons/<pk>/
# PUT    /api/lessons/<pk>/
# PATCH  /api/lessons/<pk>/
# DELETE /api/lessons/<pk>/
# ==========================================================

class LessonsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lessons.objects.select_related(
        "created_by"
    ).prefetch_related(
        "videos",
        "quiz__questions"
    )

    serializer_class = LessonsSerializer
    permission_classes = [AllowAny]


# ==========================================================
# QUIZ
# GET  /api/lessons/<lesson_id>/quiz/
# POST /api/lessons/<lesson_id>/quiz/
# ==========================================================

class LessonQuizView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, lesson_id):
        try:
            quiz = Quiz.objects.prefetch_related(
                "questions"
            ).get(lesson_id=lesson_id)

        except Quiz.DoesNotExist:
            return Response({
                "message": "This lesson does not have a quiz yet."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSerializer(quiz)

        return Response(serializer.data)

    def post(self, request, lesson_id):
        try:
            lesson = Lessons.objects.get(id=lesson_id)

        except Lessons.DoesNotExist:
            return Response({
                "message": "Lesson not found."
            }, status=status.HTTP_404_NOT_FOUND)

        if Quiz.objects.filter(lesson=lesson).exists():
            return Response({
                "message": "This lesson already has a quiz."
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data["lesson"] = lesson.id

        serializer = QuizSerializer(data=data)

        if serializer.is_valid():
            quiz = serializer.save()

            return Response(
                QuizSerializer(quiz).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================================
# QUIZ DETAIL
# GET    /api/quizzes/<pk>/
# PUT    /api/quizzes/<pk>/
# PATCH  /api/quizzes/<pk>/
# DELETE /api/quizzes/<pk>/
# ==========================================================

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.prefetch_related("questions")
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


# ==========================================================
# ADD QUESTION
# POST /api/quizzes/<quiz_id>/questions/
# ==========================================================

class QuizQuestionListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, quiz_id):
        questions = QuizQuestion.objects.filter(
            quiz_id=quiz_id
        )

        serializer = QuizQuestionSerializer(
            questions,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)

        except Quiz.DoesNotExist:
            return Response({
                "message": "Quiz not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizQuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(quiz=quiz)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================================
# QUESTION DETAIL
# GET    /api/questions/<pk>/
# PUT    /api/questions/<pk>/
# PATCH  /api/questions/<pk>/
# DELETE /api/questions/<pk>/
# ==========================================================

class QuizQuestionDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    permission_classes = [AllowAny]


# ==========================================================
# LESSON VIDEOS
# POST /api/lessons/<lesson_id>/videos/
# GET  /api/lessons/<lesson_id>/videos/
# ==========================================================

class LessonVideoListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, lesson_id):
        videos = LessonsVideo.objects.filter(
            lesson_id=lesson_id
        )

        serializer = LessonsVideoSerializer(
            videos,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request, lesson_id):
        try:
            lesson = Lessons.objects.get(id=lesson_id)

        except Lessons.DoesNotExist:
            return Response({
                "message": "Lesson not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonsVideoSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(lesson=lesson)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================================
# DELETE VIDEO
# DELETE /api/videos/<pk>/
# ==========================================================

class LessonVideoDetailView(generics.DestroyAPIView):
    queryset = LessonsVideo.objects.all()
    serializer_class = LessonsVideoSerializer
    permission_classes = [AllowAny]



class QuizScoreView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, user_id):
        if not User.objects.filter(id=user_id).exists():
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        scores = QuizScore.objects.filter(user_id=user_id)
        serializer = QuizScoreSerializer(scores, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuizScoreSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)

            return Response(
                {
                    "message": "Quiz score submitted successfully!",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        title = request.query_params.get("title")

        if not title:
            return Response(
                {"error": "Quiz title is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = QuizScore.objects.filter(
            user=user,
            title=title
        ).delete()

        if deleted_count == 0:
            return Response(
                {"error": "No quiz score found for this lesson."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "message": "Quiz attempt deleted successfully.",
                "deleted_count": deleted_count
            },
            status=status.HTTP_200_OK
        )
        
        
class AllStudentsQuizScoresView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        scores = QuizScore.objects.select_related(
            "user"
        ).all().order_by("-time_submitted")

        serializer = StudentsQuizScoreSerializer(
            scores,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        
        
        


# UPLOAD FILE
class FileUploadCreateView(generics.CreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [AllowAny]


# LIST ALL UPLOADED FILES
class FileUploadListView(generics.ListAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [AllowAny]


# VIEW FILE DETAILS
class FileUploadDetailView(generics.RetrieveAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [AllowAny]


# VIEW / OPEN FILE
class FileUploadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        uploaded_file = get_object_or_404(FileUpload, pk=pk)

        if not uploaded_file.file:
            return Response(
                {"error": "File not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "id": uploaded_file.id,
            "title": uploaded_file.title,
            "file_url": request.build_absolute_uri(uploaded_file.file.url),
            "file_extension": uploaded_file.file_extension,
            "date_posted": uploaded_file.date_posted,
        })


# DOWNLOAD FILE
class FileUploadDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        uploaded_file = get_object_or_404(FileUpload, pk=pk)

        if not uploaded_file.file:
            return Response(
                {"error": "File not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return FileResponse(
            uploaded_file.file.open('rb'),
            as_attachment=True,
            filename=uploaded_file.file.name.split('/')[-1]
        )


# DELETE FILE
class FileUploadDeleteView(generics.DestroyAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [AllowAny]

    def perform_destroy(self, instance):
        instance.file.delete(save=False)
        instance.delete()
        
        
# ==========================================================
# STUDENT MANAGEMENT
# GET  /api/students/
# POST /api/students/
# ==========================================================

class StudentsListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(
            is_staff=False,
            is_superuser=False
        ).order_by("first_name", "username")

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            student = serializer.save()

            return Response(
                {
                    "message": "Student registered successfully!",
                    "student": UserSerializer(student).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================================
# STUDENT DETAILS / DELETE
# GET    /api/students/<pk>/
# DELETE /api/students/<pk>/
# ==========================================================

class StudentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(
            is_staff=False,
            is_superuser=False
        )
