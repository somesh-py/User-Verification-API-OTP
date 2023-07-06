from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import math,random
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

#formate to create-user,password,is_verified,otp,otp_created_at are in last of the source code

@api_view(['POST'])
def create_user(request):
        email=request.data.get('email')
        password=request.data.get('password')

        otp=get_otp()

        data=User.objects.create(email=email,password=password,otp=otp)

        email=data.email
        subject="OTP for Verification"
        message=f"One-Time-Password is : {otp} Valid for 3 min only & usable only once on Verification T&C apply."
        email_from=settings.EMAIL_HOST_USER
        to=email
        recipient_list = [to,]
        send_mail( subject, message, email_from, recipient_list )
        return Response({'msg':'Check your Email and Verify your Id Using OTP'})



@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    user = User.objects.filter(email=email, otp=otp).first()
    if user and not user.is_verified and is_valid_otp(user.otp_created_at):
        user.is_verified = True
        user.save()
        return Response({'msg': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
    
    user.delete()
    return Response({'msg': 'Invalid OTP.Your Otp Was Expire To Generate New Otp Register Your-Self Again'}, status=status.HTTP_400_BAD_REQUEST)

def is_valid_otp(created_at):
    expiry_time = created_at + timedelta(minutes=3)
    current_time = timezone.now()
    return current_time < expiry_time

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    User.objects.filter(email=email,password=password).exists()
    user=User.objects.get(email=email)

    if user:

        if user.is_verified==True:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            user.token=access_token
            user.save()
            return Response({'access_token':access_token})
        
        else:
          return Response({'msg':'user is not verified plz verify your identitiy'})

    else:
        return Response({'msg': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({'msg':'datat retrive','data':serializer.data}, status=status.HTTP_200_OK)

def get_otp():
    digits="0123456789"
    OTP=""
    for i in range(5):
        OTP+=digits[math.floor(random.random()*10)]
    return OTP

# formate to create-user

# {
# "email":" enter your email ",
# "password":" enter password"
# }

# formate to verify-otp

# {
# "email":" enter your email ",
# "otp":" enter otp from email "
# }

# formate to login

# {
# "email":" enter your email ",
# "password":" enter password"
# }