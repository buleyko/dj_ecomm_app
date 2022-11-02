from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path, 
    include,
    re_path,
)
from django.conf.urls import (
    handler404, 
    handler500, 
    handler403, 
    handler400,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include([ # <slug:alias>/
        # path('account/', include('ecomm.apps.account.urls', namespace='account')),
        path('', include('ecomm.apps.fnd.urls', namespace='fnd')),
    ])),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'ecomm.apps.fnd.views.fnd.error_404'
handler500 = 'ecomm.apps.fnd.views.fnd.error_500'
handler403 = 'ecomm.apps.fnd.views.fnd.error_403'
handler400 = 'ecomm.apps.fnd.views.fnd.error_400'
