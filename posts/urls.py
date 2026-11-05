from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('posts/nuevo/', views.PostCreateView.as_view(), name='create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('posts/<int:pk>/editar/', views.PostUpdateView.as_view(), name='update'),
    path('posts/<int:pk>/eliminar/', views.PostDeleteView.as_view(), name='delete'),
]
