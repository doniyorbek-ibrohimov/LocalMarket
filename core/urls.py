from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Local Market API",
      default_version='v1',
      description="Test",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="doniyorbek.info@gmail.com"),
      license=openapi.License(name="Codial License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('api/', include('product.urls')),
    path('orders/', include('order.urls')),
]

urlpatterns += [
    path('token/', token_obtain_pair),
    path('token/refresh/', token_refresh),
]

urlpatterns += [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

