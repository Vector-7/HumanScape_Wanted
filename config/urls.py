from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions


# swagger view
schema_view = get_schema_view(
    openapi.Info(
        title = 'HumanScape Icreate',
        default_version = '0.1.0',
        description = '',
        terms_of_service = '',
        
    ),
    public = True,
    permission_classes = [permissions.AllowAny]
)

swagger_urlpatterns = [
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]

# If prod, collect static file for display swagger to client
# 배포할때, 웹파일 긁어모을 때만 사용
"""
if not settings.DEBUG:
	swagger_urlpatterns.append(
		static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	)
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/icreat', include('apps.icreat.urls')),
    path('api/batch', include('apps.icreat_batch.urls')),
] + swagger_urlpatterns
