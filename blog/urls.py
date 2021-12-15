from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    # slug:pkとすることで、'localhost:8000/blog/~'の"~"に入ったものを変数pkとして使用できる
    # （slugの他、int=整数のみ, str=文字列のみがある）
    path("<int:pk>/", views.article, name="article"),
    path("tags/<slug:slug>/", views.tags, name="tags"),
    path("", views.index, name="blog"),
    path('<slug:pk>/like/', views.like),
    path('<slug:pk>/fav/', views.add_favorite),
    path('add/', views.add_post, name='add'),
    path('edit/<int:pk>', views.edit_post, name='edit'),
    path('my/posts/', views.my_posts, name='my_posts'),
]
