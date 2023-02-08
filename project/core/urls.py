"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts.views import ApiVerifyEmailView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

media_urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

api_urlpatterns = [
    path(
        "accounts/registration/account-confirm-email/",
        ApiVerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "accounts/registration/",
        include("dj_rest_auth.registration.urls"),
    ),
    path(
        "accounts/",
        include("dj_rest_auth.urls"),
    ),
]

urlpatterns = [
    path("api/v1/", include(api_urlpatterns)),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("activities/", include("activities.urls")),
    path("caregivers/", include("caregivers.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("circles/", include("circles.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
] + media_urlpatterns

handler404 = "error_handling.views.handler404"
handler500 = "error_handling.views.handler500"
handler403 = "error_handling.views.handler403"
handler400 = "error_handling.views.handler400"
