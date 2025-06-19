import uuid
import json
import hmac
import hashlib
import requests

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Payment
from listings.models import Property
from checkout.models import Cart


class InitializePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user, is_paid=False)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found or already paid'}, status=404)

        amount = int(float(cart.total_price()) * 100)
        reference = str(uuid.uuid4())

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            'email': user.email,
            'amount': amount,
            'reference': reference,
            'callback_url': settings.PAYSTACK_CALLBACK_URL, # frontend
        }

        try:
            response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
            res_data = response.json()

            if res_data.get("status") is True:
                Payment.objects.create(user=user, cart=cart, amount=amount, reference=reference)
                return Response({
                    "payment_url": res_data["data"]["authorization_url"],
                    "reference": reference
                }, status=status.HTTP_200_OK)

            return Response(res_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'Payment initialization failed', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        reference = request.GET.get('reference')
        if not reference:
            return Response({"error": "Reference not provided"}, status=400)

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }

        response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
        res_data = response.json()

        if res_data['data']['status'] == "success":
            try:
                payment = Payment.objects.get(reference=reference)
                payment.verified = True
                payment.save()

                cart = payment.cart
                cart.is_paid = True
                cart.save()

                for item in cart.items.all():
                    item.property.is_active = False
                    item.property.save()

                return Response({"message": "Payment verified successfully."})
            except Payment.DoesNotExist:
                return Response({"error": "Payment not found."}, status=404)

        return Response({"error": "Payment verification failed."}, status=400)


# @csrf_exempt
# def paystack_webhook(request):
#     paystack_secret = settings.PAYSTACK_SECRET_KEY.encode()
#     signature = request.META.get('HTTP_X_PAYSTACK_SIGNATURE')

#     payload = request.body
#     expected_signature = hmac.new(paystack_secret, payload, hashlib.sha512).hexdigest()

#     if signature != expected_signature:
#         return HttpResponse(status=400)

#     event = json.loads(payload.decode('utf-8'))

#     if event['event'] == 'charge.success':
#         data = event['data']
#         reference = data['reference']
#         metadata = data.get('metadata', {})
#         property_id = metadata.get('property_id')

#         try:
#             property_obj = Property.objects.get(id=property_id)
#             property_obj.is_active = False
#             property_obj.save()
#         except Property.DoesNotExist:
#             pass  # Log error optionally

#     return HttpResponse(status=200)

