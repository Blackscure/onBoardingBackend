from authentication.api.serializers import RegisterSerializer, UserSerializer
from authentication.models import User
from rest_framework import  permissions, views, status
from rest_framework.response import Response # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated # type: ignore
from role.models import Role

from django.contrib.auth import get_user_model

from utils.paginator import CustomPaginator

User=get_user_model()

class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Provide valid details to register',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            user_type_id = data.get('user_type_id')

            # Check if user_type exists in Role model using ID
            try:
                user_type = Role.objects.get(id=user_type_id)
            except Role.DoesNotExist:
                return Response({
                    'status': False,
                    'message': 'Invalid user type. Choose a valid role.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Additional validation checks
            if not email:
                return Response({'status': False, 'message': 'Email cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'status': False, 'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            if not first_name:
                return Response({'status': False, 'message': 'First Name cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

            if not last_name:
                return Response({'status': False, 'message': 'Last Name cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

            if not password:
                return Response({'status': False, 'message': 'Password cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user with the validated role
            user = User.objects.create(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                user_type=user_type  # Set user_type as Role instance
            )
            user.set_password(password)
            user.save()

            serializer = UserSerializer(user)
            return Response({
                'status': True,
                'message': 'Registration successful',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"An error occurred during registration: {str(e)}")
            return Response({
                'status': False,
                'message': 'An error occurred during registration'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoginApiView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'success': False, 'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                data = {
                    'success': True,
                    'data': {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'user': UserSerializer(user).data
                    }
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({'success': False, 'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        

class SignOutApiView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can log out

    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response({'success': False, 'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Attempt to decode and blacklist the refresh token
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token to prevent further use
                return Response({'success': True, 'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'success': False, 'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetTokenView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer



    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            print(email)
            print(password)

            # Attempt to authenticate using email and password
            users = authenticate(username=email, password=password)
            

            if users is not None:
                # Authentication succeeded
                refresh = RefreshToken.for_user(users)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                data = {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': UserSerializer(users).data
                }

                return Response(data, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            # Handle exceptions here, you can log the error or return a specific response
            print(f"An error occurred during login: {str(e)}")
            return Response({
                'status': False,
                'message': 'An error occurred during login',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch user_type and print it for debugging
            user_role = getattr(request.user, 'user_type', None)
            user_role_name = getattr(user_role, 'role_name', None)  # Get the role name if it exists
            print(f"Authenticated User: {request.user.username}, User Role: {user_role_name}")

            # Check if the user has a role of 'Admin'
            if user_role_name == 'Admin':
                # Retrieve all users if the check passes
                users = User.objects.all()

                # Apply custom pagination
                paginator = CustomPaginator()
                paginated_users = paginator.paginate_queryset(users, request, view=self)
                serializer = UserSerializer(paginated_users, many=True)

                # Return paginated response
                return paginator.get_paginated_response(serializer.data)
            else:
                # If user_role is not 'Admin', deny access
                return Response({
                    "status": False,
                    "message": "Access denied"
                }, status=403)

        except Exception as e:
            # Handle unexpected errors
            return Response({
                'status': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)



class EditUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            getuser = User.objects.get(pk=pk)
            serializer = UserSerializer(getuser, data=request.data)
            if not serializer.is_valid():
                return Response({"status": "error","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
            serializer.save()
     
            return Response({
                'status': True,
                'message':'Update Has been successful.',
                'data': serializer.data
            })


        except Exception as e:
                return Response({
                'status':False,
                'message':'We were not able to get registered users .',
                "error": str(e)
            })