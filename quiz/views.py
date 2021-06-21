from django.shortcuts import render, get_object_or_404
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.decorators import action
import django.contrib.auth.password_validation as validators
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import parsers
from django.utils import timezone
from django.middleware import csrf
from rest_framework import viewsets
from quiz.serializers import (
    Subject, Question,
    QuestionSerializer, SubjectSerializer,
    Paper, PaperSerializer, LoginSerializer,
    UserSerializer, User,
    Quiz, QuizSerializer, 
    QuizResultSerializer, QuizResult
)

class QuestionPage(pagination.BasePagination):
    page_size = 20

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    # authentication_classes = [authentication.TokenAuthentication, authentication.BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    # pagination_class = QuestionPage



class ByQuestion(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        try:
            subject = Subject.objects.get(pk=id)
        except Subject.DoesNotExist:
            return Response({'error': 'Does Not Exist.'}, status=status.HTTP_404_NOT_FOUND)

        queryset = subject.questions.all()
        serializer = QuestionSerializer(instance=queryset, many=True)
        return Response(serializer.data)

class SubjectViews(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

class PaperViews(ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    # permission_classes = [permissions.IsAuthenticated]

# class LoginView(views.APIView):
#     def post(self, request):
#         print(csrf.get_token(request))
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data.get('username', None)
#             password = serializer.validated_data.get('password', None)
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 try:
#                     t = Token.objects.get(user=user)
#                 except Token.DoesNotExist:
#                     t = Token.objects.create(user=user)
#                 auth_token = t.key
#                 return Response({'message': "You're logged in.", 'token': auth_token})
#             else:
#                 return Response({'error': "Correct credentials were not provided"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(views.APIView):
#     def get(self, request):
#         if request.user.is_authenticated:
#             logout(request)
#             return Response({'message': "You're logout"})
#         else:
#             return Response({'error': 'Not Logged In.'})

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    filterset_fields = ['archived']


# class QuizView(views.APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, test_id):
#         test = get_object_or_404(Quiz, pk=test_id)
#         current_time = timezone.now()

#         if current_time >= test.starting_time and current_time <= test.ending_time:
#             serilizer = QuizSerializer(instance=test)
#             return Response(serilizer.data)
#         else:
#             return Response({'error': 'The Test Does\'t started or has been ended.'}, status=status.HTTP_400_BAD_REQUEST)
        
class QuizResultView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = QuizResult.objects.all()
        serializer = QuizResultSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = dict(request.data)
        # print(data)
        for key, val in data.items():
            data[key] = val[0]
        data['user'] = request.user.pk
        serializer = QuizResultSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeView(views.APIView):
    def get(self, request):
        current_time = timezone.now()
        return Response({'time': str(current_time)})

class SubjectByPaper(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, paper_id):
        paper = get_object_or_404(Paper, pk=paper_id)
        queryset = paper.subject_set.all()
        serializer = PaperSerializer(queryset, many=True)
        return Response(serializer.data)
