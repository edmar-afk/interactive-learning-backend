from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LessonsListCreateView,
    LessonsDetailView,
    LessonQuizView,
    QuizDetailView,
    QuizQuestionListCreateView,
    QuizQuestionDetailView,
    LessonVideoListCreateView,
    LessonVideoDetailView,
    QuizScoreView,
    AllStudentsQuizScoresView,

    # File Upload
    FileUploadCreateView,
    FileUploadListView,
    FileUploadDetailView,
    FileUploadView,
    FileUploadDownloadView,
    FileUploadDeleteView,
    StudentsListCreateView,
    StudentDetailView,
    VideoListView,
    VideoUploadView,
    VideoViewView,
    VideoDeleteView,
)


urlpatterns = [
    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # Lessons
    path("lessons/", LessonsListCreateView.as_view(), name="lessons"),
    path("lessons/<int:pk>/", LessonsDetailView.as_view(), name="lesson-detail"),

    # Lesson Quiz
    path("lessons/<int:lesson_id>/quiz/", LessonQuizView.as_view(), name="lesson-quiz"),

    # Quiz Management
    path("quizzes/<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),

    # Quiz Questions
    path("quizzes/<int:quiz_id>/questions/", QuizQuestionListCreateView.as_view(), name="quiz-questions"),
    path("questions/<int:pk>/", QuizQuestionDetailView.as_view(), name="question-detail"),

    # Lesson Videos
    path("lessons/<int:lesson_id>/videos/", LessonVideoListCreateView.as_view(), name="lesson-videos"),
    path("videos/<int:pk>/", LessonVideoDetailView.as_view(), name="video-detail"),

    # Quiz Scores
    path("quiz-scores/<int:user_id>/", QuizScoreView.as_view(), name="quiz-scores"),
    path("quiz-scores/all/", AllStudentsQuizScoresView.as_view(), name="all-students-quiz-scores"),

    # File Upload
    path("files/upload/", FileUploadCreateView.as_view(), name="file-upload"),
    path("files/", FileUploadListView.as_view(), name="file-list"),
    path("files/<int:pk>/", FileUploadDetailView.as_view(), name="file-detail"),
    path("files/<int:pk>/view/", FileUploadView.as_view(), name="file-view"),
    path("files/<int:pk>/download/", FileUploadDownloadView.as_view(), name="file-download"),
    path("files/<int:pk>/delete/", FileUploadDeleteView.as_view(), name="file-delete"),
    
    path("students/", StudentsListCreateView.as_view(), name="students"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    
    
    
    path(
        "videos/",
        VideoListView.as_view(),
        name="video-list"
    ),

    path(
        "videos/upload/",
        VideoUploadView.as_view(),
        name="video-upload"
    ),

    path(
        "videos/<int:pk>/view/",
        VideoViewView.as_view(),
        name="video-view"
    ),

    path(
        "videos/<int:pk>/delete/",
        VideoDeleteView.as_view(),
        name="video-delete"
    ),
]