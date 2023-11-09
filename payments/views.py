import uuid
import requests

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Gateway, Payment
from subscriptions.models import Package, Subscription
from .serializers import GatewaySerializer

class GatewayView(APIView):
    def get(self):
        gateways = Gateway.objects.all()
        serializer = GatewaySerializer(gateways, many=True)
        return Response(serializer.data)
    

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        package_id = request.data.get('package')
        gateway_id = request.data.get('gateway')
        try: 
            package = Package.objects.get(pk=package_id, is_enable=True)
            gateway = Gateway.objects.get(pk=gateway_id)
        except (Package.DoesNotExist, Gateway.DoesNotExist): 
            return Response({'package or gateway does not exists!'}, status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user = request.user,
            package = package,
            gateway = gateway,
            price = package.price,
            phone_number = request.user.phone_number,
            token = str(uuid.uuid4()),
        )

        return Response({'token': payment.token, 'callback_url': 'https://mysite.com/pay/payments/'})
    
    def post(self, request):
        token = request.data.get('token')
        st = request.data.get('status')

        try: 
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if st != "bank_done_code":
            payment.status = Payment.STATUS_ERROR
            payment.save()
            return Response({'detail': 'occur some error on bank api!'}, status.HTTP_400_BAD_REQUEST)
        
        # r = requests.post('bank_verify_url', data={})
        # if r.status_code // 100 != 2:
        #     payment.status = Payment.STATUS_ERROR
        #     payment.save()
        #     return Response({'detail': 'payment verification failed!'}, status.HTTP_400_BAD_REQUEST)
        
        payment.status = Payment.STATUS_PAID
        payment.save()

        Subscription.objects.create(
            user = payment.user,
            package = payment.package,
            expire_time = timezone.now() + timezone.timedelta(payment.package.duration.days)
        )

        return Response({'detail': 'your payment is succesfull.'})
        


