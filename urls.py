from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/image/', views.serve_image, name='serve_image'),
    ]

urlpatterns = [
    path('profile/<str:user_id>/blog/', views.serve_blog, name='serve_blog'),
    
]

urlpatterns = [
    path('profile/<str:user_id>/video/', views.serve_video, name='serve_video'),
]

