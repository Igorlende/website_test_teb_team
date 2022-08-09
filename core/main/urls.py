from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_request, name='login'),
    path('api/register', views.register_user_request, name='register_user'),
    path('api/get_clicks_and_conversations_by_custom_date', views.get_clicks_and_conversations_by_custom_date,
         name='get_clicks_and_conversations_by_custom_date'),
    path('logout/', LogoutView.as_view(next_page='/home'), name='logout'),
    path('', RedirectView.as_view(url='/home'))
]