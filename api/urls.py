
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
    LessonVideoDetailView, QuizScoreView, AllStudentsQuizScoresView
)


urlpatterns = [

    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # Lessons
    path("lessons/", LessonsListCreateView.as_view(), name="lessons"),
    path("lessons/<int:pk>/", LessonsDetailView.as_view(), name="lesson-detail"),

    # Lesson Quiz
    path(
        "lessons/<int:lesson_id>/quiz/",
        LessonQuizView.as_view(),
        name="lesson-quiz"
    ),

    # Quiz management
    path(
        "quizzes/<int:pk>/",
        QuizDetailView.as_view(),
        name="quiz-detail"
    ),

    # Quiz Questions
    path(
        "quizzes/<int:quiz_id>/questions/",
        QuizQuestionListCreateView.as_view(),
        name="quiz-questions"
    ),
    path(
        "questions/<int:pk>/",
        QuizQuestionDetailView.as_view(),
        name="question-detail"
    ),

    # Lesson Videos
    path(
        "lessons/<int:lesson_id>/videos/",
        LessonVideoListCreateView.as_view(),
        name="lesson-videos"
    ),
    path(
        "videos/<int:pk>/",
        LessonVideoDetailView.as_view(),
        name="video-detail"
    ),
    
    
    path(
        "quiz-scores/<int:user_id>/",
        QuizScoreView.as_view(),
        name="quiz-scores"
    ),
    
    path(
        "quiz-scores/all/",
        AllStudentsQuizScoresView.as_view(),
        name="all-students-quiz-scores"
    ),
]
