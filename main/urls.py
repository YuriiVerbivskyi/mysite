from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from rest_framework import permissions



schema_view = get_schema_view(
    openapi.Info(
        title="E-Queue API",
        default_version='v1',
        description="API documentaion",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('queues/', views.QueueListView.as_view(), name='queues'),
    path('queues/<int:pk>/', views.QueueDetailView.as_view(), name='queue_detail'),
    path('entries/', views.QueueEntryListView.as_view(), name='queue_entries'),
    path('entries/<int:pk>/', views.QueueEntryDetailView.as_view(), name='queue_entry_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify'),
    path('register/', views.Register.as_view(), name='register_api'),
    path('login/', views.LoginView.as_view(), name='login_api'),
    path('profile/', views.user_profile, name='user_profile_api'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
