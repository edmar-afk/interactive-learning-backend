
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Lessons(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="N/A")
    content = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LessonsVideo(models.Model):
    lesson = models.ForeignKey(
        Lessons,
        on_delete=models.CASCADE,
        related_name="videos"
    )
    video_file = models.FileField(
        upload_to="lesson_videos/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "avi", "mov"]
            )
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Video for {self.lesson.title}"


class Quiz(models.Model):
    lesson = models.OneToOneField(
        Lessons,
        on_delete=models.CASCADE,
        related_name="quiz"
    )
    title = models.CharField(max_length=255, default="Lesson Quiz")
    description = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quiz for {self.lesson.title}"


class QuizQuestion(models.Model):

    TRUE_FALSE = "TRUE_FALSE"
    ENUMERATION = "ENUMERATION"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    FILL_BLANK = "FILL_BLANK"

    QUESTION_TYPES = [
        (TRUE_FALSE, "True or False"),
        (ENUMERATION, "Enumeration"),
        (MULTIPLE_CHOICE, "Multiple Choice"),
        (FILL_BLANK, "Fill in the Blank"),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES
    )

    question = models.TextField()

    # Used only for multiple choice.
    # Example: ["A. Manila", "B. Cebu", "C. Davao", "D. Iloilo"]
    options = models.JSONField(default=list, blank=True)

    # Stores accepted answers.
    # True/False: ["True"]
    # Enumeration: ["Answer 1", "Answer 2", "Answer 3"]
    # Multiple Choice: ["A"]
    # Fill in the Blank: ["correct answer", "another accepted answer"]
    correct_answers = models.JSONField(default=list)

    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.question_type}: {self.question[:50]}"




class QuizScore(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quiz_scores"
    )

    title = models.CharField(max_length=255)
    score = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)

    time_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.score}"

    class Meta:
        ordering = ["-time_submitted"]