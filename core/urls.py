from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.templatetags.static import static as static_tag
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path('api/', include('products.urls')),
    path('api/users/', include('users.urls')),
    path('api/cart/', include('cart.urls'))
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
)

# 👉 favicon.ico na raiz
urlpatterns += [
    path(
        "favicon.ico",
        RedirectView.as_view(url=static_tag("favicon.ico"))
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)