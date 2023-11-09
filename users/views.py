import random
import uuid

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Device


class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response(status.HTTP_400_BAD_REQUEST)
        
        try:
            User.objects.get(phone_number=phone_number)
            return Response({'detail': 'User already registered!'}, status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)
            
        Device.objects.create(user=user)

        code = random.randint(10000, 99999)

        cache.set(str(phone_number), code, 60 * 2)

        return Response({"code": code})
    

class GetTokenView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = int(request.data.get('code'))

        if not phone_number or not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        cached_code = cache.get(str(phone_number))

        if code != cached_code:
            return Response({'detail': f'Code is not match!'}, status.HTTP_400_BAD_REQUEST)
        
        token = str(uuid.uuid4())

        return Response({'token': token})

