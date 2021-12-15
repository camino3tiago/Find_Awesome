from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'mysite'


urlpatterns = [
    
    path('', views.index, name='home'),
    # path('landing/', views.landing, ),  # Materializeを使用したトップページ

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('favorite/', views.favorite, name='favorite'),
    path('contact/', views.ContactView.as_view(), name='contact'),

    path('about/', views.about, name='about'),

]