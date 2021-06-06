from django.contrib import admin
from django.urls import path, include

# routs of all apps to be here
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include("authentication.urls")),
]
