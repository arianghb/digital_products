from django.test import TestCase, override_settings
from django.test import Client
from django.urls import path

import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User

class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        email = request.data['email']
        try:
            User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            User.objects.create_user(phone_number=phone_number, email=email)
            code = random.randint(10000, 99999)
            return Response(data={"code": code}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_409_CONFLICT)


urlpatterns = [
    path('register/', RegisterView.as_view())
]

@override_settings(ROOT_URLCONF=__name__)
class test(TestCase):
    def test(self):
        c = Client()
        response = c.post('/register/', {'phone_number': '989903396362'})   
        self.assertEqual(response, 'test')
