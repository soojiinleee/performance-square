import debug_toolbar
import mimetypes

from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 서비스 url
    path('user/', include('user.urls')),
    path('performance/', include('performance.urls')),
    path('review/', include('review.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    mimetypes.add_type("application/javascript", ".js", True)
    urlpatterns = [
        # rest_framework viewable page
        path('api-auth/', include('rest_framework.urls')),

        # debug toolbar
        path("__debug__/", include(debug_toolbar.urls)),

        # swagger 문서
        path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
        path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui", ),
        path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc", ),
    ] + urlpatterns