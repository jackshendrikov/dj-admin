from django.urls import path
from django.views.generic import TemplateView

from .views import get_requests, post_requests

app_name = 'api'
urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('api/v1/get/', get_requests, name='get_request'),   # GET API
    path('api/v1/post/', post_requests, name='post_request')   # POST API
]
