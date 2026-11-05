
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Lessons,
    LessonsVideo,
    Quiz,
    QuizQuestion, QuizScore
)


# ==========================================================
# USER SERIALIZERS
# ==========================================================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "username",
            "email",
            "password",
            
        ]

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Username is already taken."
            )
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Email is already registered."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
        ]

# ==========================================================
# VIDEO SERIALIZER
# ==========================================================

class LessonsVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonsVideo
        fields = "__all__"


# ==========================================================
# QUESTION SERIALIZER
# ==========================================================


class QuizQuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = QuizQuestion
        fields = [
            "id",
            "quiz",
            "question_type",
            "question",
            "options",
            "correct_answers",
            "points",
            "order",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

    def validate(self, data):
        question_type = data.get(
            "question_type",
            getattr(self.instance, "question_type", None)
        )
        options = data.get(
            "options",
            getattr(self.instance, "options", [])
        )
        answers = data.get(
            "correct_answers",
            getattr(self.instance, "correct_answers", [])
        )

        if not isinstance(answers, list) or not answers:
            raise serializers.ValidationError({
                "correct_answers": "Provide at least one correct answer."
            })

        if not all(isinstance(a, str) and a.strip() for a in answers):
            raise serializers.ValidationError({
                "correct_answers": "Answers must be non-empty strings."
            })

        if question_type == QuizQuestion.TRUE_FALSE:
            if len(answers) != 1 or answers[0].strip().lower() not in ["true", "false"]:
                raise serializers.ValidationError({
                    "correct_answers": 'Use ["True"] or ["False"].'
                })
            if options:
                raise serializers.ValidationError({
                    "options": "True/False does not need options."
                })

        elif question_type == QuizQuestion.MULTIPLE_CHOICE:
            if not isinstance(options, list) or len(options) < 2:
                raise serializers.ValidationError({
                    "options": "Provide at least two choices."
                })

            if not all(isinstance(o, str) and o.strip() for o in options):
                raise serializers.ValidationError({
                    "options": "Choices must be non-empty strings."
                })

            if len(answers) != 1:
                raise serializers.ValidationError({
                    "correct_answers": "Provide exactly one correct option."
                })

            valid_labels = [
                chr(65 + i) for i in range(len(options))
            ]

            if answers[0].strip().upper() not in valid_labels:
                raise serializers.ValidationError({
                    "correct_answers": "Use A, B, C, D, etc."
                })

        elif question_type in [
            QuizQuestion.ENUMERATION,
            QuizQuestion.FILL_BLANK
        ]:
            if options:
                raise serializers.ValidationError({
                    "options": "This question type does not need options."
                })

        return data



# ==========================================================
# QUIZ SERIALIZER
# ==========================================================

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "lesson",
            "title",
            "description",
            "questions",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

    def validate_questions(self, value):
        if not value:
            raise serializers.ValidationError(
                "A quiz must contain at least one question."
            )
        return value

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")

        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            QuizQuestion.objects.create(
                quiz=quiz,
                **question_data
            )

        return quiz

    def update(self, instance, validated_data):
        questions_data = validated_data.pop("questions", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if questions_data is not None:
            instance.questions.all().delete()

            for question_data in questions_data:
                QuizQuestion.objects.create(
                    quiz=instance,
                    **question_data
                )

        return instance


# ==========================================================
# LESSON SERIALIZER
# ==========================================================

class LessonsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source="created_by",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    videos = LessonsVideoSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = Lessons
        fields = [
            "id",
            "user_id",
            "created_by",
            "title",
            "description",
            "content",
            "videos",
            "quiz",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_by",
            "videos",
            "quiz",
            "created_at",
            "updated_at"
        ]



class QuizScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizScore
        fields = [
            "id",
            "user",
            "title",
            "score",
            "status",
            "comment",
            "time_submitted",
        ]
        read_only_fields = ["id", "user", "time_submitted"]
        
        
class StudentsQuizScoreSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )

    user_id = serializers.IntegerField(
        source="user.id",
        read_only=True
    )

    class Meta:
        model = QuizScore
        fields = [
            "id",
            "user_id",
            "first_name",
            "title",
            "score",
            "status",
            "comment",
            "time_submitted",
        ]