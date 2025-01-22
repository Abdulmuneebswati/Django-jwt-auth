from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        error_message = serializer.errors.get("non_field_errors", ["Invalid login details."])[0]
        return Response(
            {
                "success": False,
                "message": "Login failed.",
                "errors": error_message,  # Include validation errors
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class GetUserView(APIView):

    def get(self, request, userId):
        if request.user.id != userId:
            return Response(
                {"success": False, "message": "Unauthorized access."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(id=userId)
            serializer = UserSerializer(user, context={'exclude_products': True})
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)