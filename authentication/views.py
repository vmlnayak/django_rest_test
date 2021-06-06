from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions, generics, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from rest_framework import exceptions
from authentication.serializers import RegisterSerializer, LoginSerializer
from authentication.models import User

"""
This API is to authenticate the user to get his registration/profile details
"""


class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})


""" 
This is the view created for the registration of user with exclusion of authentication
Note: username and email id must be unique 
"""


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Login view is created so that user can login with email and password 
after login with correct credentials user will get his details with auth token
"""


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, Try again"}, status=status.HTTP_401_UNAUTHORIZED)


"""
This API will be used to get all users.
right now the access to all user is given only to admin so admin token is required for this API
"""


class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email']

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RegisterSerializer(queryset, many=True)
        return Response(serializer.data)


"""
This API will enable the registered user to change his details with valid auth token
"""


class UpdateUserAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "user updated successfully", 'user': serializer.data})

            else:
                return Response({"message": "failed", "details": serializer.errors})
        else:
            raise exceptions.AuthenticationFailed('Invalid Token or user id')


"""
This API will be used by Admin user to search the details of users  
Right now filter fields are email and username
you can search by any word
"""
class UserSearchFilterAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']
