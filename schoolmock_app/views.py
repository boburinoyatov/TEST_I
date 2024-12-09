from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from .models import Test, Question, AnswerOption, StudentAnswer
from .serializers import *
from .forms import *


# ViewSet для управления тестами

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
          test = self.get_object()
          if test.is_finished:
              return Response({'error': 'Test is already finished.'}, status=status.HTTP_400_BAD_REQUEST)

          # Retrieve student details from the request
          user = request.user
          if not user:
              return Response({'error': 'Student information is required.'}, status=status.HTTP_400_BAD_REQUEST)

          # Check if the student exists, if not, create a new one
          student, created = Student.objects.get_or_create(
              student=user,
              defaults={
                  'first_name': student_data['first_name'],
                  'last_name': student_data['last_name'],
                  'school': student_data['school'],
                  'student_class': student_data['student_class'],
              }
          )

          answers = request.data.get('answers')
          total_points = 0
          response_data = []

          for ans in answers:
              try:
                  question = Question.objects.get(id=ans['question_id'])
                  correct_answer = AnswerOption.objects.filter(question=question, is_correct=True).first()

                  points_awarded = 1 if correct_answer and ans['answer_id'] == correct_answer.id else 0

                  # Save the student's answer and points
                  student_answer = StudentAnswer.objects.create(
                      student=student,
                      test=test,
                      question=question,
                      answer_option_id=ans['answer_id'],
                      points_awarded=points_awarded,
                      text_answer=ans.get('text_answer', None)  # In case of open-ended questions
                  )

                  total_points += points_awarded
                  response_data.append({
                      'question_id': question.id,
                      'points_awarded': points_awarded
                  })

              except ObjectDoesNotExist:
                  return Response({'error': 'Question or answer does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

          test.is_finished = True
          test.finished_at = timezone.now()
          test.save()

          return Response({'status': 'answers submitted', 'total_points': total_points, 'details': response_data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def test_by_id(self, request):
          test_id = request.query_params.get('test_id')
          test = Test.objects.filter(id=test_id).first()
          if not test:
              return Response({'error': 'Invalid test ID'}, status=status.HTTP_404_NOT_FOUND)

          serializer = self.get_serializer(test)
          return Response(serializer.data)

def test(request):
    return render(request, 'test.html')

def home(request):
    return render(request, 'index.html',)