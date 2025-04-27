from django.urls import path
from .views import Suggest_View

urlpatterns = [
    path('analyze/', Suggest_View.as_view(), name='analyze'),
]