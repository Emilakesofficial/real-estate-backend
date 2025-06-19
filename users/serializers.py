from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.contrib.auth.hashers import make_password 


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code','currency_code', 'currency_symbol']
                
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',]

    def to_internal_value(self, data): # is a DRF serializer class method that allows us to customize our validation
        allowed_fields = set(self.fields.keys())
        received_fields = set(data.keys())

        disallowed_fields = received_fields - allowed_fields
        if disallowed_fields:
            raise serializers.ValidationError(
                {field: "You are not allowed to update this field." for field in disallowed_fields}
            )

        return super().to_internal_value(data)

        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    phone_number = serializers.CharField(required=False)
    role = serializers.CharField(read_only = True)
    country = serializers.SerializerMethodField(read_only=True)
    profile_image = serializers.ImageField(use_url=True, required=True)
    class Meta:
        model = Profile
        fields = ['user','role', 'country', 'profile_image','phone_number']
        
    def get_country(self, obj):
        return obj.country.name if obj.country else None
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)
    country_id = serializers.IntegerField(write_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    role_display = serializers.CharField(source='profile.role', read_only=True)
    country = CountrySerializer(source='profile.country', read_only=True)
    profile_image_url = serializers.ImageField(source='profile.profile_image', read_only=True)
    phone_number_display = serializers.CharField(source='profile.phone_number', read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password', 'confirm_password',
            'role', 'country_id', 'profile_image', 'phone_number',
            'role_display', 'country', 'profile_image_url', 'phone_number_display'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Passwords do not match')

        if len(password) < 8:
            raise serializers.ValidationError({"Password": "Password must be at least 8 characters long"})

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one number')

        if not any(char.isupper() for char in password):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')

        special_characters = "!@#$%^&*()-_=+[]{}|;:',.<>?/~`"
        if not any(char in special_characters for char in password):
            raise serializers.ValidationError('Password must contain at least one special character')

        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("This email is already taken.")
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        country_id = validated_data.pop('country_id')
        phone_number = validated_data.pop('phone_number', '')
        profile_image = validated_data.pop('profile_image', None)
        validated_data.pop('confirm_password')

        validated_data['email'] = validated_data['email'].lower()

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'], 
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        # Update the profile (auto-created by signal)
        profile = user.profile
        profile.role = role
        profile.phone_number = phone_number
        profile.profile_image = profile_image

        try:
            country = Country.objects.get(pk=country_id)
            profile.country = country
        except Country.DoesNotExist:
            raise serializers.ValidationError({"country_id": "Invalid country ID."})

        profile.save()

        return user

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(source='profile.profile_image', required=False)
    phone_number = serializers.CharField(source='profile.phone_number', required=False)


    class Meta:
        model = User
        fields = ['profile_image', 'phone_number']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Do NOT allow name or role changes
        # No User fields are updated here

        # Update Profile fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance

class VerifyOldPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required = True)
    
    def validate_old_password(self, data):
        user = self.context['request'].user
        if not user.check_password(data):
            raise serializers.ValidationError('Old password incorrect')
        return data
    
class VerifyOTPSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    
    def validate(self, data):
        user = self.context['request'].user
        otp = data.get('code')
        
        try:
            otp_obj = PasswordOTP.objects.get(user=user)
        except PasswordOTP.DoesNotExist:
            raise serializers.ValidationError({'code':'No OTP found, request a new one.'})
        
        if not otp_obj.is_valid(otp):
            raise serializers.ValidationError({"code": "Invalid or expired OTP."})
        
        # delete otp after use
        otp_obj.delete()
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if new_password != confirm_password:
            raise serializers.ValidationError('passwords does not match')
        
        if len(new_password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long"})

        if not any(char.isdigit() for char in new_password):
            raise serializers.ValidationError('Password must contain at least one number')

        if not any(char.isupper() for char in new_password):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')
        
        if not any(char.islower() for char in new_password):
            raise serializers.ValidationError('Password must contain at least one lowercase letter')
        
        special_characters = "!@#$%^&*()-_=+[]{}|;:',.<>?/~`"
        if not any(char in special_characters for char in new_password):
            raise serializers.ValidationError('Password must contain at least one special character')
        return data 

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    def validate(self, data):
        new_password = data.get('new_password')
        if len(new_password) < 8:
                raise serializers.ValidationError({"password": "Password must be at least 8 characters long"})

        if not any(char.isdigit() for char in new_password):
            raise serializers.ValidationError('Password must contain at least one number')

        if not any(char.isupper() for char in new_password):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')
        
        if not any(char.islower() for char in new_password):
            raise serializers.ValidationError('Password must contain at least one lowercase letter')
        
        special_characters = "!@#$%^&*()-_=+[]{}|;:',.<>?/~`"
        if not any(char in special_characters for char in new_password):
            raise serializers.ValidationError('Password must contain at least one special character')
        return data 

class PasscodeSerializer(serializers.ModelSerializer):
    passcode = serializers.CharField(write_only=True)
    confirm_passcode = serializers.CharField(write_only=True)
    class Meta:
        model = Profile
        fields = ['passcode', 'confirm_passcode']
        
    def validate(self, data):
        passcode = data.get('passcode')
        confirm_passcode = data.get('confirm_passcode')
        
        if passcode != confirm_passcode:
            raise serializers.ValidationError('details does not match')
        
        if not passcode.isdigit():
            raise serializers.ValidationError('details must contain only digits')
        
        if len(passcode) != 6:
            raise serializers.ValidationError('details must be exactly 6 digits')
        
        # Hash the passcode before saving
        data['passcode'] = make_password(passcode)
        return data
        
    def update(self, instance, validated_data):
        instance.passcode = validated_data['passcode']
        instance.save()
        return instance

        
    
