from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views as main_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="E-Queue API",
      default_version='v1',
      description="API documentation for E-Queue",
      contact=openapi.Contact(email="your@email.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', main_views.home, name='home'),
    path('register/', main_views.register_user, name='register_page'),
    path('profile/', main_views.user_profile, name='user_profile'),
    path('login/', main_views.login_page, name='login_page'),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
