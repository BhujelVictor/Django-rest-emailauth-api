from rest_framework import serializers
from authentication.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from authentication.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    # For confirm password field in Registration Request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        
        model = User
        fields = ['email','name','tc','password','password2']
        extra_kwargs ={
            'password': {'write_only':True}
        }
    # password and confirm password2 validation
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(password)
        user.save()
        return data

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UId', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Passowrd Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+ uid +"/"+ token
            print('Password reset link', link)

            # Send Email
            body = "Click to reset your password " + link
            data = {
                "subject": "Reset your password",
                "body": body,
                "to_email": user.email,
            }
            Util.send_email(data)
            return data
        else:
            raise serializers.ValidationError("Email is not registered")
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Passwords do not match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not valid or expired')
            user.set_password(password)
            user.save()
            return data
        
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not valid or expired')


        

        
    