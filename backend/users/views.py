from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SignUpSerializer, LogInSerializer
from .models import User


class SignUpView(APIView):
    """View for registration user"""

    def post(self, request):
        """
        Registrate user and return response 
        about success registration or about fail
        """

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BASREQUEST)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


# class LogInView(APIView):
#     """View for login user."""

#     def post(self, request):
        
#         serializer = LogInSerializer(data=request.data)
#         if serializer.is_valid():
#             