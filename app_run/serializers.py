from django.contrib.auth.models import User
from rest_framework import serializers

from app_run.models import Run, AthleteInfo, Challenges


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserShortSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        if obj.is_superuser:
            return None
        return "coach" if obj.is_staff else "athlete"

    def get_runs_finished(self, obj):
        return Run.objects.filter(athlete=obj, status='finished').count()


class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = AthleteInfo
        fields = ['user_id', 'goals', 'weight']


class ChallengesSerializer(serializers.ModelSerializer):
    athlete_id = serializers.IntegerField(source='athlete.id', read_only=True)
    athlete_username = serializers.CharField(source='athlete.username', read_only=True)

    class Meta:
        model = Challenges
        fields = ['id', 'full_name', 'athlete_id', 'athlete_username', 'created_at']
