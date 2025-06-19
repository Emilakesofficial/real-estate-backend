import random
from datetime import timedelta 
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
import string
from .serializers import *
from .models import *
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.contrib.auth.hashers import make_password # to hash passcode
from rest_framework.permissions import AllowAny


def generate_token():
    return get_random_string(length=6, allowed_chars=string.digits + string.ascii_uppercase)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = generate_token()
            EmailVerificationToken.objects.update_or_create(
                user=user,
                defaults={'token': token, 'created_at': timezone.now()}
            )

            # Send email
            send_mail(
                subject="Verify your email",
                message=f"Hello {user.first_name},\n\nYour verification code is: {token}",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False
            )

            return Response({"message": "User created. Check your email for verification code."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email").strip().lower()
        token = request.data.get("token")

        if not email or not token:
            return Response({"error": "Email and token are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            token_obj = EmailVerificationToken.objects.get(user=user, token=token)
        except EmailVerificationToken.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        if not token_obj.is_valid():
            return Response({"error": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark user profile as verified
        user.profile.is_email_verified = True
        user.profile.save()
        token_obj.delete()  # Clean up used token

        return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
class ResendEmailView(APIView): 
    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        if not email:
            return Response({"error": "Email is required!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            if user.profile.is_email_verified:
                return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)

            # Generate a new 4-character alphanumeric token
            token = get_random_string(length=4, allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

            # Save or update token
            EmailVerificationToken.objects.update_or_create(
                user=user,
                defaults={
                    'token': token,
                    'created_at': timezone.now()
                }
            )

            # Send verification email
            send_mail(
                subject='Verify Your Email',
                message=f"""
Hello {user.first_name}!

Use the code below to verify your email address:

Verification Code: {token}

This code will expire in 15 minutes. If you didn’t request this, please ignore this email.
""",
                from_email=None,  # Set this to your default email if needed
                recipient_list=[user.email],
                fail_silently=False
            )

            return Response({"message": "Verification email resent. Please check your inbox."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username', '').strip().lower()
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.profile.is_email_verified:
                    return Response({'error':'Email not verified'})
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message":f"{username} logged in successfully",
                    "access_token":str(refresh.access_token),
                    "refresh_token":str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({"Message":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":"No user for this credentials"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def generate_otp():
    return str(random.randint(100000, 999999))

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists
            return Response({"message": "If the email exists, an OTP has been sent."}, status=status.HTTP_200_OK)

        otp = generate_otp()
        PasswordResetOTP.objects.create(user=user, otp=otp)

        # Send the OTP via email
        send_mail(
            "Your Password Reset OTP",
            f"Your OTP code is {otp}. It expires in 10 minutes.",
            [email],
            fail_silently=False,
        )

        return Response({"message": "If the email exists, an OTP has been sent."}, status=status.HTTP_200_OK)

class VerifyPasswordOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp, is_verified=False).last()

            if not otp_obj or otp_obj.is_expired():
                return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

            otp_obj.is_verified = True
            otp_obj.save()

            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, is_verified=True).last()

            if not otp_obj or otp_obj.is_expired():
                return Response({"error": "OTP not verified or expired."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            # Invalidate used OTP
            otp_obj.delete()

            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "Logout successful"
            }, status=status.HTTP_205_RESET_CONTENT)  
        except Exception as e:
            return Response({ "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CountryView(APIView):
    
    def get(self, request):
        try:
            countries = Country.objects.all()
            serializer = CountrySerializer(countries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            serializer = CountrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountryUpdateView(APIView):
    def put(self, request, pk):
        country = get_object_or_404(Country, pk=pk)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        country = get_object_or_404(Country, pk=pk)
        serializer = CountrySerializer(country, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOldPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = VerifyOldPasswordSerializer(data=request.data, context={'request':request})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            #OTP
            user = request.user
            otp = ''.join([str(random.randint(0,9)) for i in range(4)])
            expires_at = timezone.now() + timedelta(minutes=5)
            
            # save or update OTP
            PasswordOTP.objects.update_or_create(
                user = user,
                defaults = {'otp':otp, 'expires_at':expires_at}
            )
            
            # send email
            send_mail(
                subject = 'OTP',
                message = f'Your OTP is {otp}. It expires in 5 minutes',
                from_email= None,
                recipient_list=[user.email]
                
            )
            return Response({'detail':'OTP sent to your email'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class VerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = VerifyOTPSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                return Response({'detail':'OTP verified.You can now change password'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                new_password = serializer.validated_data['new_password']
                user.set_password(new_password) # hashing the password
                user.save()
                return Response({'message':'password changed successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PasscodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = PasscodeSerializer(data=request.data)
            if serializer.is_valid():
                # HASH THE PASSWORD AND SAVE TO PROFILE
                profile = request.user.profile
                profile.passcode = make_password(serializer.validated_data['passcode'])
                profile.save()
                return Response({"message": "Passcode set successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
