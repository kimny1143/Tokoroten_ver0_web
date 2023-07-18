from django.urls import path
from . import views
from .views import delete_file

urlpatterns = [
    path('', views.index, name='index'),
    path('delete_file/<int:file_id>/', delete_file, name='delete_file'),

]
