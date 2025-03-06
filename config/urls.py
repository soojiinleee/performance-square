import debug_toolbar
import mimetypes

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('performance/', include('performance.urls')),
    path('review/', include('review.urls')),
]

if settings.DEBUG:
    mimetypes.add_type("application/javascript", ".js", True)
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns