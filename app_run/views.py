from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import Run
from .serializers import RunSerializer, UserSerializer


class StandartPagination(PageNumberPagination):
    # page_size = 10  # Количество объектов на странице по умолчанию (не обязательный параметр)
    page_size_query_param = 'size'
    # max_page_size = 100  # Ограничиваем максимальное количество объектов на странице


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()

    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    ordering = ['id']
    pagination_class = StandartPagination


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]  # Подключаем SearchFilter здесь
    search_fields = ['first_name', 'last_name']  # Указываем поля по которым будет вестись поиск
    ordering_fields = ['date_joined']
    ordering = ['id']
    pagination_class = StandartPagination

    def get_queryset(self):
        qs = self.queryset.exclude(is_superuser=True)  # исключаем админов
        user_type = self.request.query_params.get("type")

        if user_type == "coach":
            qs = qs.filter(is_staff=True)
        elif user_type == "athlete":
            qs = qs.filter(is_staff=False)

        return qs


@api_view(['GET'])
def preview_view(request):
    company_name = settings.COMPANY_NAME
    slogan = settings.SLOGAN
    contacts = settings.CONTACTS
    return Response({'company_name': company_name,
                     'slogan': slogan,
                     'contacts': contacts,
                     })


class StartStatusAPIView(APIView):
    def get(self, request, run_id, *args, **kwargs):
        run = get_object_or_404(Run, id=run_id)
        return Response(
            {"status": run.status},
            status=status.HTTP_200_OK,
        )

    def post(self, request, run_id, *args, **kwargs):
        run = get_object_or_404(Run, id=run_id)

        if run.status != 'init':
            return Response(
                {"error": "Забег уже начат или завершён."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        run.status = 'in_progress'
        run.save()
        return Response(
            {"message": "Забег запущен", "status": run.status},
            status=status.HTTP_200_OK,
        )


class StopStatusAPIView(APIView):
    def get(self, request, run_id, *args, **kwargs):
        run = get_object_or_404(Run, id=run_id)
        return Response(
            {"status": run.status},
            status=status.HTTP_200_OK,
        )

    def post(self, request, run_id, *args, **kwargs):
        run = get_object_or_404(Run, id=run_id)

        if run.status != 'in_progress':
            return Response(
                {"error": "Нельзя завершить забег, который не запущен или уже завершён."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        run.status = 'finished'
        run.save()
        return Response(
            {"message": "Забег завершён", "status": run.status},
            status=status.HTTP_200_OK,
        )
