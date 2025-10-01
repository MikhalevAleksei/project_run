from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings


@api_view(['GET'])
def preview_view(request):
    company_name = settings.COMPANY_NAME
    slogan = settings.SLOGAN
    contacts = settings.CONTACTS
    return Response({'company_name': company_name,
                     'slogan': slogan,
                     'contacts': contacts,
                     })
