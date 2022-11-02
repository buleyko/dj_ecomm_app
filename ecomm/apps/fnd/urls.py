from django.urls import path, include
from ecomm.apps.fnd.views import (
    fnd,
)

app_name = 'fnd'

urlpatterns = [
    path('', fnd.home, name='home'),
    path('options/', fnd.options, name='options'),
    path('change-language/<str:lang>/', fnd.change_language, name='change_language'),
]