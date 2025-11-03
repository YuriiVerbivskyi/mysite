from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from rest_framework import status
from django.shortcuts import render

def register_user(request):
    return render(request, 'register.html')


def home(request):
    return render(request, 'index.html')

class QueueListView(APIView):
    def get(self, request):
        return Response({"queues": []})

class QueueDetailView(APIView):
    def get(self, request, pk):
        return Response({"queue": pk})

class QueueEntryListView(APIView):
    def get(self, request):
        return Response({"entries": []})

class QueueEntryDetailView(APIView):
    def get(self, request, pk):
        return Response({"entry": pk})

# def get_csrf_token(request):
#     return HttpResponse("CSRF endpoint")

class Register(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {"message": "Success registration", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

def user_profile(request):
    return HttpResponse("User profile endpoint")
