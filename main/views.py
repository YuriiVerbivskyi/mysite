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

def get_last_transs():
        headers = {
            "accept": "application/json",
            "x-token": "usqbA76ff6U0Fi6Z_QL3t2Xmh42lYCOUQ9h9v2PW51nM"
        }
        account_id = "WEzuUgHoGQVlmHaHagiU0w" 
        start = 1759622400
        end = 1762214400
        url = f"https://api.monobank.ua/personal/statement/{account_id}/{start}/{end}"
        r = requests.get(url, headers=headers)
        ans = r.json()
        last_transs = []
        try:
            for i in ans:
                last_transs.append({i["description"]: i["amount"]})
            return last_transs
        except Exception as e:
            return e

class MonoData(APIView):
    def get(self, requests, data):
        if data == "trans":
            print("gettting last transs..")
            last_trns = get_last_transs()
            print(last_trns)


        elif data == "balance":
            print("current balance")
        else:
            print("doesn't exist")
            return redirect("/")

        return JsonResponse({"status": "ok"})



