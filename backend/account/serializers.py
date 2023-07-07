from rest_framework import serializers
from account.models import User  #user from our custom user model
from django.utils.encoding import smart_str ,force_bytes ,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator   #to reset password
from django.forms import ValidationError #to enable your view to raise a validationError if somethiong goes wrong during registration,login,resetpassword,sending email verification or usage of the application
from account.utils import Util
#to register a user we create a user registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    #we are writing this because we need to confirm password field in our Registration Request
    password2 =serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc']
        extra_kwargs ={
            'password':{'write_only':True}
        }

    #validating password  and confirm password during registration   
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password and Confirm password doesn't match")
        return attrs

    def create(self,validate_data):
        return User.objects.create_user(**validate_data)


#to login a user we create the userloginserializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=225)
    class Meta:
        model = User
        fields = ['email','password'] 


#to create a user profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']


#to change a user password
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225,
    style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=225,style=
    {'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and Confirm password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


#to enable django send the reset password token to the user Email
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields =['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password Reset Token',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link',link)
            #Send Email
            body ='Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
           # Util.send_email(data)
            return attrs
        else:
            raise ValidationError('You are not a  Registered User') ###
        # return super().validate(attrs)

#to change a user get a link on their email when they reset their  password
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225,
    style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=225,style=
    {'input_type':'password2'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError("password and Confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise  serializers.ValidationError('Token is not Valid or Expired') ##
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not Valid or Expired') ##