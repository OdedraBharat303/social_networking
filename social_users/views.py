from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import CustomUser, FriendRequest
from django.db.models import Q
import random
import string
from rest_framework.authtoken.models import Token
from django.db.utils import IntegrityError
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# CustomUser = get_user_model()

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            if not password:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            name = email.split('@')[0]
            user = CustomUser.objects.create_user(email=email, password=password)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email').lower()  # Make email case-insensitive
            password = serializer.validated_data.get('password')
            user = CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                # token, created = Token.objects.get_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({'token': str(refresh.access_token)})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, search_keyword):
        serializer = UserSearchSerializer(data={"search_keyword": search_keyword})
        if serializer.is_valid():
            search_keyword = serializer.validated_data['search_keyword']
            print(search_keyword,"::::::::::::::")
            users = CustomUser.objects.filter(
                Q(email__iexact=search_keyword) | Q(name__icontains=search_keyword)
            ).distinct()[:10]
            user_data = CustomUserSerializer(users, many=True).data
            return Response({"results": user_data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, to_user_id):
        # Rate limit is enforced here
        if request.user.sent_friend_requests.count() >= 3:
            return Response({'error': 'You have reached the maximum number of friend requests allowed per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        to_user = CustomUser.objects.get(pk=to_user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'error': 'Friend request already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)

class AcceptFriendRequestView(APIView):
    def post(self, request, from_user_id):
        from_user = CustomUser.objects.get(pk=from_user_id)
        friend_request = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()

        if not friend_request:
            return Response({'error': 'No pending friend request from this user.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.is_accepted = True
        friend_request.save()

        return Response({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)

class RejectFriendRequestView(APIView):
    def post(self, request, from_user_id):
        from_user = CustomUser.objects.get(pk=from_user_id)
        friend_request = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()

        if not friend_request:
            return Response({'error': 'No pending friend request from this user.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.delete()
        return Response({'message': 'Friend request rejected successfully'}, status=status.HTTP_200_OK)


class ListFriendsView(APIView):
    def get(self, request):
        friends = CustomUser.objects.filter(received_friend_requests__from_user=request.user)
        friend_data = CustomUserSerializer(friends, many=True).data
        return Response({"friends": friend_data}, status=status.HTTP_200_OK)

class ListPendingFriendRequestsView(APIView):
    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user)
        pending_data = CustomUserSerializer([request.from_user for request in pending_requests], many=True).data
        return Response({"pending_requests": pending_data}, status=status.HTTP_200_OK)

