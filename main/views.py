from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from .serializers import CustomUserSerializer, QueueSerializer, QueueEntrySerializer, NotificationSerializer
from .permissions import IsQueueOwnerOrAdmin, IsAuthenticatedOrReadOnly
from .models import Queue, QueueEntry, Notification, CustomUser
from .utils import send_notification_email


def register_user(request):
    return render(request, 'register.html')


def home(request):
    return render(request, 'index.html')


class QueueListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queues = Queue.objects.all()
        serializer = QueueSerializer(queues, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QueueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueueDetailView(APIView):
    permission_classes = [IsQueueOwnerOrAdmin]

    def get_object(self, pk):
        return Queue.objects.get(pk=pk)

    def get(self, request, pk):
        queue = self.get_object(pk)
        serializer = QueueSerializer(queue)
        return Response(serializer.data)

    def put(self, request, pk):
        queue = self.get_object(pk)
        self.check_object_permissions(request, queue)
        serializer = QueueSerializer(queue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queue = self.get_object(pk)
        self.check_object_permissions(request, queue)
        queue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QueueEntryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = QueueEntry.objects.all()
        serializer = QueueEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QueueEntrySerializer(data=request.data)
        if serializer.is_valid():
            entry = serializer.save(user=request.user)
            position = QueueEntry.objects.filter(queue=entry.queue).count()
            entry.position = position
            entry.save()

            try:
                if position == 1:
                    subject = "Ти наступний до здачі завдання!"
                    message = f"Вітаю {request.user.first_name or request.user.username}!\n\n{entry.queue.name}\n\nБудь готовим, орієнтовний час 2-3хв\n\nНомер: {position}"
                    notification_type = 'ready'
                else:
                    subject = "Запис у чергу успішний"
                    message = f"Вітаю {request.user.first_name or request.user.username}!\n\nТи записався(лась) у чергу: {entry.queue.name}\n\nТвій номер у черзі: {position}\n\nОчікуй свою чергу."
                    notification_type = 'queue_joined'

                send_notification_email(request.user, subject, message, notification_type)
            except Exception as e:
                print(f"Помилка відправки email при записі в чергу: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueueEntryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return QueueEntry.objects.get(pk=pk)

    def get(self, request, pk):
        entry = self.get_object(pk)
        serializer = QueueEntrySerializer(entry)
        return Response(serializer.data)

    def put(self, request, pk):
        entry = self.get_object(pk)
        serializer = QueueEntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        entry = self.get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                send_notification_email(
                    user,
                    "Реєстрація успішна",
                    f"Вітаю {user.first_name or user.username}!\n\nWelcome to E-Queue!\n\nТвій аккаунт успішно створений.\n\nКористувач: {user.username}\nПошта: {user.email}",
                    'registration'
                )
            except Exception as e:
                print(f"Помилка відправки email при реєстрації: {e}")

            return Response(
                {"message": "Success registration", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "role": getattr(request.user, 'role', 'student')
    })
