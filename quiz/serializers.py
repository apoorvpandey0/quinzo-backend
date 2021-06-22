from rest_framework import serializers
from quiz.models import Subject, Question, Paper, Quiz, QuizResult
from django.contrib.auth import password_validation
from rest_framework import validators
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]

    def validate(self, data):
        branches = ['IT']
        if len(data['username']) != 12:
            raise serializers.ValidationError("Please enter a valid Enrollment no. eg. 0101IT910XX")
        if "0101" not in data['username'][0:4]:
            raise serializers.ValidationError("The registrations are only open to the students of UIT RGPV")
        if data['username'][4:6] not in branches:
            raise serializers.ValidationError("The registrations are only open to the students IT department")
        try:
            password_validation.validate_password(data['password'])
        except Exception as e:
            raise serializers.ValidationError(e)
        return data
    
    def create(self, validated_data):
        return User.objects.create_user(
            username = validated_data.get('username'),
            password = validated_data.get('password'),
            email = validated_data.get('email', ''),
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', '')
        )

class QuizResultSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = QuizResult
        fields = '__all__'
    
    # def create(self, validated_data):
    #     # user = CurrentUserDefault()
    #     return QuizResult(**validated_data)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Subject

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Paper


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = [
            'title',
            'options',
            'subject', 
            'marks',
            'answer',
            'date'
        ]
        read_only_fields = ['answer', 'marks', 'date']

    def get_options(self, obj):
        return {
            'option_a': obj.option_a,
            'option_b': obj.option_b,
            'option_c': obj.option_c,
            'option_d': obj.option_d
        }
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    

        
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Quiz
        fields = '__all__'
        # depth = 1
