from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.predictor, name = 'predictor'),
]

urlpatterns += staticfiles_urlpatterns()