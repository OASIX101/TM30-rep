from django.urls import path, include
from . import views 

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='logout'),
    path('x-auth/', include('djoser.urls')),
    path('x-access/', include('djoser.urls.jwt')),
]