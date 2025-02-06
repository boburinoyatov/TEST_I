from rest_framework import serializers
from .models import Test, Question, AnswerOption, StudentAnswer

# Сериализатор для вариантов ответа
class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text']

# Сериализатор для вопросов с вариантами ответа
class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']

# Сериализатор для теста с вопросами
class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'questions']

class TestStudentAnswersSerializer(serializers.ModelSerializer):
    student_answers = AnswerOption()

    class Meta:
        model = Test
        fields = ['test_id', 'student_answers', 'finished_at']
