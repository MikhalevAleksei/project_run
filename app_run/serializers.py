from decimal import Decimal, InvalidOperation

from django.contrib.auth.models import User
from rest_framework import serializers, status

from app_run.models import Run, AthleteInfo, Challenge, Position


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserShortSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = [
            'id',
            'created_at',
            'comment',
            'athlete',
            'athlete_data',
            'status',
        ]


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'date_joined',
            'username',
            'last_name',
            'first_name',
            'type',
            'runs_finished',
        ]

    def get_type(self, obj):
        if obj.is_superuser:
            return None

        if obj.is_staff:
            return 'coach'

        return 'athlete'

    def get_runs_finished(self, obj):
        return Run.objects.filter(
            athlete=obj,
            status='finished'
        ).count()


class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AthleteInfo
        fields = [
            'user_id',
            'goals',
            'weight',
        ]


class ChallengeSerializer(serializers.ModelSerializer):
    athlete_id = serializers.IntegerField(source='athlete.id', read_only=True)
    athlete_username = serializers.CharField(source='athlete.username', read_only=True)

    class Meta:
        model = Challenge
        fields = [
            'id',
            'full_name',
            'athlete_id',
            'athlete_username',
            'created_at',
        ]

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = [
            'id',
            'run',
            'latitude',
            'longitude',
        ]

    def validate_run(self, value):
        if value.status != Run.STATUS_IN_PROGRESS:
            raise serializers.ValidationError(
                "Координаты можно добавлять только для забега в статусе in_progress."
            )
        return value

    def validate_latitude(self, value):
        if value < -90.0 or value > 90.0:
            raise serializers.ValidationError(
                "latitude должна находиться в диапазоне от -90.0 до 90.0."
            )

        self.validate_decimal_places(value, 'latitude')

        return value

    def validate_longitude(self, value):
        if value < -180.0 or value > 180.0:
            raise serializers.ValidationError(
                "longitude должна находиться в диапазоне от -180.0 до 180.0."
            )

        self.validate_decimal_places(value, 'longitude')

        return value

    def validate_decimal_places(self, value, field_name):
        try:
            decimal_value = Decimal(str(value))
        except InvalidOperation:
            raise serializers.ValidationError(
                f"{field_name} должно быть числом."
            )

        decimal_places = abs(decimal_value.as_tuple().exponent)

        if decimal_places > 4:
            raise serializers.ValidationError(
                f"{field_name} может иметь не больше 4 знаков после запятой."
            )