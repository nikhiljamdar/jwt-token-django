from django.urls import path
from . import views


urlpatterns=[
    path('',views.login_view,name='home'),
    path('generate_token/',views.generate_token,name='generate_token'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout_view,name='logout'),
    
]